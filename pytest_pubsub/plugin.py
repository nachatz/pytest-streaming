from pytest import Config, Parser, OptionGroup, Session
from pytest_pubsub.pubsub.publisher import GCPPublisher
from pytest_pubsub.config import Configuration, MarkerConfiguration


def pytest_addoption(parser: Parser) -> None:
    """Adds options to the pytest command line.

    The ini options are added to the pytest command line options
    so that they can be set from the ini file.

    Args:
        parser: pytest parser object
    """
    _: OptionGroup = parser.getgroup("pytest-pubsub", "Pub/Sub plugin options")

    parser.addini(
        Configuration.GLOBAL_TOPICS,
        "Comma separated list of global Pub/Sub topics to create at session start - default is None and is a line list",
        type="linelist",
        default=[],
    )

    parser.addini(
        Configuration.GLOBAL_DELETE,
        "Whether to delete global topics after session finishes (True/False) - default is True",
        type="bool",
        default=False,
    )

    parser.addini(
        Configuration.PROJECT_ID,
        "GCP project ID to use for Pub/Sub topics (local only) - default is 'default'",
        type="string",
        default="default",
    )

    parser.addini(
        Configuration.RUN_EMULATOR,
        "Whether to run the Pub/Sub emulator before tests (True/False) - default is False",
        default=False,
    )


def pytest_configure(config: Config) -> None:
    config.addinivalue_line(
        "markers", f"{MarkerConfiguration.pubsub}: Create specified Pub/Sub topics automatically for the test. "
    )


def pytest_sessionstart(session: Session) -> None:
    """Creates global topics if specified in the ini file.

    Also, starts the pubsub emulator if the option is set.

    Args:
        session: pytest session object
    """
    config: Config = session.config
    global_topics_to_create = config.getini(Configuration.GLOBAL_TOPICS)
    run_pubsub_emulator = config.getini(Configuration.RUN_EMULATOR)
    project_id = config.getini(Configuration.PROJECT_ID)

    if run_pubsub_emulator:
        pass

    GCPPublisher().setup_testing_topics(project_id, global_topics_to_create)


def pytest_sessionfinish(session: Session, exitstatus: int) -> None:
    """Delete global topics at session finish if configured.

    Args:
        session: pytest session object
        exitstatus: exit status of the session
    """

    config: Config = session.config
    global_topics_to_create = config.getini(Configuration.GLOBAL_TOPICS)
    cleanup_global_topics = config.getini(Configuration.GLOBAL_DELETE)
    project_id = config.getini(Configuration.PROJECT_ID)

    if not cleanup_global_topics:
        return

    GCPPublisher().delete_testing_topics(project_id, global_topics_to_create)
