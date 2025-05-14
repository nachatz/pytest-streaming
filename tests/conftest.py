import pytest
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
