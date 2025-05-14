import pytest
from pytest import Config

from pytest_streaming.pubsub.publisher import GCPPublisher
from pytest_streaming.pulsar.client import AdminClient
from pytest_streaming.pulsar.client import PulsarClientWrapper
from tests.settings import PulsarTestSettings

pytest_plugins = ["pytester"]


@pytest.fixture(scope="session", autouse=True)
def plugin_was_loaded(pytestconfig: Config) -> None:
    """Ensures the pytest-streaming plugin is loaded."""
    assert pytestconfig.pluginmanager.hasplugin("pytest_streaming")


@pytest.fixture(scope="session")
def pulsar_settings() -> PulsarTestSettings:
    return PulsarTestSettings()


@pytest.fixture(scope="session")
def gcp_publisher() -> GCPPublisher:
    return GCPPublisher()


@pytest.fixture(scope="session")
def pulsar_client(pulsar_settings: PulsarTestSettings) -> PulsarClientWrapper:
    return PulsarClientWrapper(service_url=pulsar_settings.service_url, admin_url=pulsar_settings.admin_url)


@pytest.fixture(scope="session")
def pulsar_admin_client(pulsar_settings: PulsarTestSettings) -> AdminClient:
    return AdminClient(base_url=pulsar_settings.admin_url)
