from contextlib import ExitStack
from typing import Generator

import pytest
from pytest import Config
from pytest import FixtureRequest
from pytest import OptionGroup
from pytest import Parser
from pytest import Session

from pytest_streaming.config import Configuration
from pytest_streaming.config import Defaults
from pytest_streaming.config import MarkerConfiguration
from pytest_streaming.fixtures.markers import pubsub_setup_marker
from pytest_streaming.pubsub.publisher import GCPPublisher


def pytest_addoption(parser: Parser) -> None:
    """Adds options to the pytest command line.

    The ini options are added to the pytest command line options
    so that they can be set from the ini file.

    Args:
        parser: pytest parser object
    """
    _: OptionGroup = parser.getgroup("pytest-streaming", "Pub/Sub plugin options")

    parser.addini(
        Configuration.PUBSUB_GLOBAL_TOPICS,
        "Comma separated list of global Pub/Sub topics to create at session start - default is None and is a line list",
        type="linelist",
        default=[],
    )

    parser.addini(
        Configuration.PUBSUB_GLOBAL_DELETE,
        "Whether to delete global topics after session finishes (True/False) - default is True",
        type="bool",
        default=False,
    )

    parser.addini(
        Configuration.PUBSUB_PROJECT_ID,
        "GCP project ID to use for Pub/Sub topics (local only) - default is 'default'",
        type="string",
        default=Defaults.PROJECT_ID,
    )


def pytest_configure(config: Config) -> None:
    config.addinivalue_line(
        "markers", f"{MarkerConfiguration.pubsub}: Create specified Pub/Sub topics automatically for the test. "
    )


def pytest_sessionstart(session: Session) -> None:
    """Creates global topics if specified in the ini file.

    Args:
        session: pytest session object
    """
    config: Config = session.config
    global_topics_to_create = config.getini(Configuration.PUBSUB_GLOBAL_TOPICS)
    project_id = config.getini(Configuration.PUBSUB_PROJECT_ID)

    if not global_topics_to_create:
        return

    GCPPublisher().setup_testing_topics(project_id, global_topics_to_create)


def pytest_sessionfinish(session: Session, exitstatus: int) -> None:
    """Delete global topics at session finish if configured.

    Args:
        session: pytest session object
        exitstatus: exit status of the session
    """

    config: Config = session.config
    global_topics_to_create = config.getini(Configuration.PUBSUB_GLOBAL_TOPICS)
    cleanup_global_topics = config.getini(Configuration.PUBSUB_GLOBAL_DELETE)
    project_id = config.getini(Configuration.PUBSUB_PROJECT_ID)

    if not cleanup_global_topics:
        return

    GCPPublisher().delete_testing_topics(project_id, global_topics_to_create)


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
