import pytest

from pytest_streaming.config import Defaults
from pytest_streaming.pulsar.client import PulsarClientWrapper
from tests.pulsar.enums import PulsarTopicName
from tests.settings import PulsarTestSettings


class TestPulsarPlugin:
    @pytest.fixture()
    def settings(self) -> PulsarTestSettings:
        return PulsarTestSettings()

    @pytest.fixture()
    def pulsar_client(self, settings: PulsarTestSettings) -> PulsarClientWrapper:
        return PulsarClientWrapper(settings.service_url, settings.admin_url)

    def test_pulsar_global_create_topics(self, pulsar_client: PulsarClientWrapper) -> None:
        topics = pulsar_client.client.get_topics(
            namespace=Defaults.PULSAR_NAMESPACE.value, tenant=Defaults.PULSAR_TENANT.value
        )
        assert any(PulsarTopicName.GLOBAL_TOPIC_CREATE_ONE in topic for topic in topics)
        assert any(PulsarTopicName.GLOBAL_TOPIC_CREATE_TWO in topic for topic in topics)

    def test_pulsar_global_delete_topics(self, pulsar_client: PulsarClientWrapper) -> None:
        topics = pulsar_client.client.get_topics(
            namespace=Defaults.PULSAR_NAMESPACE.value, tenant=Defaults.PULSAR_TENANT.value
        )
        assert any(PulsarTopicName.GLOBAL_TOPIC_DELETE_ONE in topic for topic in topics)
        assert any(PulsarTopicName.GLOBAL_TOPIC_DELETE_TWO in topic for topic in topics)
