from pytest import Config
from pytest import Parser
from pytest import Session

from pytest_streaming.config import Configuration
from pytest_streaming.config import Defaults
from pytest_streaming.pulsar._models import TopicMeta
from pytest_streaming.pulsar.client import PulsarClientWrapper


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
        default=Defaults.PULSAR_AUTO_DELETE.value,
    )

    parser.addini(
        Configuration.PULSAR_SERVICE_URL,
        "Pulsar service URL",
        type="string",
        default=Defaults.PULSAR_SERVICE_URL.value,
    )

    parser.addini(
        Configuration.PULSAR_ADMIN_URL,
        "Pulsar admin URL",
        type="string",
        default=Defaults.PULSAR_ADMIN_URL.value,
    )

    parser.addini(
        Configuration.PULSAR_TENANT,
        "Pulsar tenant",
        type="string",
        default=Defaults.PULSAR_TENANT.value,
    )

    parser.addini(
        Configuration.PULSAR_NAMESPACE,
        "Pulsar namespace",
        type="string",
        default=Defaults.PULSAR_NAMESPACE.value,
    )


def pulsar_sessionstart(session: Session) -> None:
    """Creates global Pulsar topics if specified."""
    config: Config = session.config
    service_url = config.getini(Configuration.PULSAR_SERVICE_URL)
    admin_url = config.getini(Configuration.PULSAR_ADMIN_URL)
    tenant = config.getini(Configuration.PULSAR_TENANT)
    namespace = config.getini(Configuration.PULSAR_NAMESPACE)
    global_topics = config.getini(Configuration.PULSAR_GLOBAL_TOPICS)

    if not global_topics:
        return

    client = PulsarClientWrapper(service_url=service_url, admin_url=admin_url)
    try:
        topics = [TopicMeta(topic_name=topic, tenant=tenant, namespace=namespace) for topic in global_topics]
        client.setup_testing_topics(topics=topics)
    finally:
        client.close()


def pulsar_sessionfinish(session: Session) -> None:
    """Deletes global Pulsar topics if configured."""
    config: Config = session.config
    tenant = config.getini(Configuration.PULSAR_TENANT)
    namespace = config.getini(Configuration.PULSAR_NAMESPACE)
    service_url = config.getini(Configuration.PULSAR_SERVICE_URL)
    admin_url = config.getini(Configuration.PULSAR_ADMIN_URL)
    global_topics = config.getini(Configuration.PULSAR_GLOBAL_TOPICS)
    cleanup_global = config.getini(Configuration.PULSAR_GLOBAL_DELETE)

    if not cleanup_global or not global_topics:
        return

    client = PulsarClientWrapper(service_url=service_url, admin_url=admin_url)
    try:
        topics = [TopicMeta(topic_name=topic, tenant=tenant, namespace=namespace) for topic in global_topics]
        client.delete_testing_topics(topics=topics)
    finally:
        client.close()
