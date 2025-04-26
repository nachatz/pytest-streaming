from contextlib import ExitStack
from typing import Generator

import pytest
from pytest import Config
from pytest import FixtureRequest
from pytest import OptionGroup
from pytest import Parser
from pytest import Session

from pytest_streaming.config import MarkerConfiguration
from pytest_streaming.fixtures.markers import pubsub_setup_marker
from pytest_streaming.pubsub.plugin import pubsub_addoption
from pytest_streaming.pubsub.plugin import pubsub_sessionfinish
from pytest_streaming.pubsub.plugin import pubsub_sessionstart


def pytest_addoption(parser: Parser) -> None:
    """Adds options to the pytest command line.

    The ini options are added to the pytest command line options
    so that they can be set from the ini file.

    Args:
        parser: pytest parser object
    """
    _: OptionGroup = parser.getgroup("pytest-streaming", "Streaming plugin options")
    pubsub_addoption(parser)


def pytest_configure(config: Config) -> None:
    """Establish all of our marker setups.

    Args:
        config: pytest config object
    """
    config.addinivalue_line(
        "markers", f"{MarkerConfiguration.pubsub}: Create specified Pub/Sub topics automatically for the test. "
    )


def pytest_sessionstart(session: Session) -> None:
    """Creates global topics if specified in the ini file.

    Args:
        session: pytest session object
    """
    pubsub_sessionstart(session)


def pytest_sessionfinish(session: Session, exitstatus: int) -> None:
    """Delete global topics at session finish if configured.

    Args:
        session: pytest session object
        exitstatus: exit status of the session
    """
    pubsub_sessionfinish(session)


@pytest.fixture(autouse=True)
def _markers(request: FixtureRequest, pytestconfig: Config) -> Generator[None, None, None]:
    """Setup and teardown for pubsub markers.

    Args:
        request: pytest fixture request object
        pytestconfig: pytest config object
    """
    with ExitStack() as stack:
        stack.enter_context(pubsub_setup_marker(request, pytestconfig))
        yield
