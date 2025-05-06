from pytest import Config
from pytest import Parser
from pytest import Session

from pytest_streaming.config import Configuration
from pytest_streaming.config import Defaults


def pulsar_addoption(parser: Parser) -> None:
    """Adds Pulsar options to the pytest command line."""

    parser.addini(
        Configuration.PULSAR_GLOBAL_TOPICS,
        "Comma separated list of global Pulsar topics to create at session start",
        type="linelist",
        default=[],
    )

    parser.addini(
        Configuration.PULSAR_GLOBAL_DELETE,
        "Whether to delete global Pulsar topics after session finishes",
        type="bool",
        default=False,
    )

    parser.addini(
        Configuration.PULSAR_SERVICE_URL,
        "Pulsar service URL",
        type="string",
        default=Defaults.PULSAR_SERVICE_URL,
    )

    parser.addini(
        Configuration.PULSAR_TENANT,
        "Pulsar tenant",
        type="string",
        default=Defaults.PULSAR_TENANT,
    )

    parser.addini(
        Configuration.PULSAR_NAMESPACE,
        "Pulsar namespace",
        type="string",
        default=Defaults.PULSAR_NAMESPACE,
    )


def pulsar_sessionstart(session: Session) -> None:
    """Creates global Pulsar topics if specified."""
    config: Config = session.config
    service_url = config.getini(Configuration.PULSAR_SERVICE_URL)
    tenant = config.getini(Configuration.PULSAR_TENANT)
    namespace = config.getini(Configuration.PULSAR_NAMESPACE)
    global_topics = config.getini(Configuration.PULSAR_GLOBAL_TOPICS)

    if not global_topics:
        return

    client = PulsarClientWrapper(service_url=service_url)
    try:
        client.setup_testing_topics(tenant, namespace, global_topics)
    finally:
        client.close()


def pulsar_sessionfinish(session: Session) -> None:
    """Deletes global Pulsar topics if configured."""
    config: Config = session.config
    service_url = config.getini(Configuration.PULSAR_SERVICE_URL)
    tenant = config.getini(Configuration.PULSAR_TENANT)
    namespace = config.getini(Configuration.PULSAR_NAMESPACE)
    global_topics = config.getini(Configuration.PULSAR_GLOBAL_TOPICS)
    cleanup_global = config.getini(Configuration.PULSAR_GLOBAL_DELETE)

    if not cleanup_global or not global_topics:
        return

    client = PulsarClientWrapper(service_url=service_url)
    try:
        client.delete_testing_topics(tenant, namespace, global_topics)
    finally:
        client.close()
