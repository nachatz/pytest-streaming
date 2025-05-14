from pytest import Config
from pytest import Parser
from pytest import Session

from pytest_streaming.config import Configuration
from pytest_streaming.config import Defaults
from pytest_streaming.pubsub.publisher import GCPPublisher


def pubsub_addoption(parser: Parser) -> None:
    """Adds options to the pytest command line.

    The ini options are added to the pytest command line options
    so that they can be set from the ini file.

    Args:
        parser: pytest parser object
    """
    parser.addini(
        Configuration.PUBSUB_GLOBAL_TOPICS,
        "Comma separated list of global Pub/Sub topics to create at session start - default is None and is a line list",
        type="linelist",
        default=[],
    )

    parser.addini(
        Configuration.PUBSUB_GLOBAL_DELETE,
        "Whether to delete global topics after session finishes (True/False) - default is False",
        type="bool",
        default=Defaults.PUBSUB_GLOBAL_DELETE.value,
    )

    parser.addini(
        Configuration.PUBSUB_PROJECT_ID,
        "GCP project ID to use for Pub/Sub topics (local only) - default is 'default'",
        type="string",
        default=Defaults.PROJECT_ID.value,
    )

    parser.addini(
        Configuration.PUBSUB_EMULATOR_ENABLED,
        "Ensures the pubsub emulator is being used",
        type="bool",
        default=Defaults.PUBSUB_EMULATOR_ENABLED.value,
    )


def pubsub_sessionstart(session: Session) -> None:
    """Creates global topics if specified in the ini file
    for GCP pubsub.

    Args:
        session: pytest session object
    """
    config: Config = session.config
    project_id = config.getini(Configuration.PUBSUB_PROJECT_ID)
    global_topics_to_create = config.getini(Configuration.PUBSUB_GLOBAL_TOPICS)
    safety = config.getini(Configuration.PUBSUB_EMULATOR_ENABLED)
    if not global_topics_to_create:
        return

    GCPPublisher().setup_testing_topics(project_id, global_topics_to_create, safety=safety)


def pubsub_sessionfinish(session: Session) -> None:
    """Delete global topics at session finish if configured.

    Args:
        session: pytest session object
    """
    config: Config = session.config
    project_id = config.getini(Configuration.PUBSUB_PROJECT_ID)
    global_topics_to_create = config.getini(Configuration.PUBSUB_GLOBAL_TOPICS)
    cleanup_global_topics = config.getini(Configuration.PUBSUB_GLOBAL_DELETE)
    safety = config.getini(Configuration.PUBSUB_EMULATOR_ENABLED)
    if not cleanup_global_topics:
        return

    GCPPublisher().delete_testing_topics(project_id, global_topics_to_create, safety=safety)
