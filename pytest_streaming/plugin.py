from contextlib import ExitStack
from typing import Generator

import pytest
from pytest import Config
from pytest import FixtureRequest
from pytest import OptionGroup
from pytest import Parser
from pytest import Session

from pytest_streaming.abstracts.markers import BaseMarker
from pytest_streaming.pubsub.markers import PubsubMarker
from pytest_streaming.pubsub.plugin import pubsub_addoption
from pytest_streaming.pubsub.plugin import pubsub_sessionfinish
from pytest_streaming.pubsub.plugin import pubsub_sessionstart
from pytest_streaming.pulsar.fixtures import *  # noqa: F403
from pytest_streaming.pulsar.markers import PulsarMarker
from pytest_streaming.pulsar.plugin import pulsar_addoption
from pytest_streaming.pulsar.plugin import pulsar_sessionfinish
from pytest_streaming.pulsar.plugin import pulsar_sessionstart


def pytest_addoption(parser: Parser) -> None:
    """Adds options to the pytest command line.

    The ini options are added to the pytest command line options
    so that they can be set from the ini file.

    Args:
        parser: pytest parser object
    """
    _: OptionGroup = parser.getgroup("pytest-streaming", "Streaming plugin options")
    pubsub_addoption(parser)
    pulsar_addoption(parser)


def pytest_sessionstart(session: Session) -> None:
    """Creates global topics if specified in the ini file.

    Args:
        session: pytest session object
    """
    pubsub_sessionstart(session)
    pulsar_sessionstart(session)


def pytest_sessionfinish(session: Session, exitstatus: int) -> None:
    """Delete global topics at session finish if configured.

    Args:
        session: pytest session object
        exitstatus: exit status of the session
    """
    pulsar_sessionfinish(session)
    pubsub_sessionfinish(session)


def pytest_configure(config: Config) -> None:
    """Establish all of our marker setups.

    Args:
        config: pytest config object
    """
    config.addinivalue_line("markers", PubsubMarker.definition())
    config.addinivalue_line("markers", PulsarMarker.definition())


@pytest.fixture(autouse=True)
def _markers(request: FixtureRequest, pytestconfig: Config) -> Generator[None, None, None]:
    """Setup and teardown for all streaming markers.

    Args:
        request: pytest fixture request object
        pytestconfig: pytest config object
    """
    markers: list[BaseMarker] = [
        PubsubMarker(config=pytestconfig, request=request),
        PulsarMarker(config=pytestconfig, request=request),
    ]

    with ExitStack() as stack:
        for marker in markers:
            stack.enter_context(marker.impl())
        yield
