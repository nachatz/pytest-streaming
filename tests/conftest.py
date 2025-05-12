import pytest
from google.api_core.exceptions import NotFound
from pytest import Config

from pytest_streaming.pubsub.publisher import GCPPublisher
from pytest_streaming.pulsar.client import PulsarClientWrapper
from tests.pubsub.enums import PubsubProjectId
from tests.settings import PulsarTestSettings

pytest_plugins = ["pytester"]


@pytest.fixture(scope="session", autouse=True)
def plugin_was_loaded(pytestconfig: Config) -> None:
    """Ensures the pytest-streaming plugin is loaded."""
    assert pytestconfig.pluginmanager.hasplugin("pytest_streaming")


@pytest.fixture(scope="session")
def pubsub_project_ids() -> list[str]:
    """Returns a list of project IDs used in tests sourced
    from ProjectIds enum."""
    return [member.value for member in PubsubProjectId]


@pytest.fixture(scope="session")
def pulsar_settings() -> PulsarTestSettings:
    return PulsarTestSettings()


@pytest.fixture(scope="session")
def publisher() -> GCPPublisher:
    return GCPPublisher()


@pytest.fixture(scope="session")
def pulsar_client(pulsar_settings: PulsarTestSettings) -> PulsarClientWrapper:
    return PulsarClientWrapper(service_url=pulsar_settings.service_url, admin_url=pulsar_settings.admin_url)


@pytest.fixture(scope="session", autouse=True)
def destroy_pubsub_topics(pubsub_project_ids: list[str], publisher: GCPPublisher) -> None:
    """Ensures the pubsub topics are cleansed prior to each test.

    Args:
        pubsub_project_ids (fixture: list[str]): List of project IDs to clean up.
        publisher (fixture: GCPPublisher): The GCPPublisher instance to use for cleanup.
    """
    for project_id in pubsub_project_ids:
        project_path = f"projects/{project_id}"
        found_topics = publisher.list_topics(request={"project": project_path})
        found_topics = [topic.name for topic in found_topics]

        for topic in found_topics:
            try:
                publisher.delete_topic(topic=topic)
            except NotFound:
                ...


@pytest.fixture(scope="session", autouse=True)
def destroy_pulsar_topics(pulsar_client: PulsarClientWrapper) -> None:
    """Ensures the pulsar topics are cleaned up prior to the test suite running.

    Args:
        pulsar_client (fixture: PulsarClientWrapper): The Pulsar client instance to use for cleanup.
    """
    # TODO: add support for custom namespace and tenants
    pulsar_client._delete_tenant(tenant="public")
