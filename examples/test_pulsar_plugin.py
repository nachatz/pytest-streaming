from pytest_streaming.config import Defaults
from pytest_streaming.pulsar.client import PulsarClientWrapper
from tests.pulsar.enums import PulsarTopicName
from tests.settings import PulsarTestSettings


class TestPulsarPlugin:
    def test_pulsar_global_create_topics(self) -> None:
        pulsar_settings = PulsarTestSettings()
        pulsar_client = PulsarClientWrapper(
            service_url=pulsar_settings.service_url, admin_url=pulsar_settings.admin_url
        )
        topics = pulsar_client._get_topics(namespace=Defaults.PULSAR_NAMESPACE, tenant=Defaults.PULSAR_TENANT)
        assert any(PulsarTopicName.GLOBAL_TOPIC_CREATE_ONE in topic for topic in topics)
        assert any(PulsarTopicName.GLOBAL_TOPIC_CREATE_TWO in topic for topic in topics)

    def test_pulsar_global_delete_topics(self) -> None:
        pulsar_settings = PulsarTestSettings()
        pulsar_client = PulsarClientWrapper(
            service_url=pulsar_settings.service_url, admin_url=pulsar_settings.admin_url
        )
        topics = pulsar_client._get_topics(namespace=Defaults.PULSAR_NAMESPACE, tenant=Defaults.PULSAR_TENANT)
        assert any(PulsarTopicName.GLOBAL_TOPIC_DELETE_ONE in topic for topic in topics)
        assert any(PulsarTopicName.GLOBAL_TOPIC_DELETE_TWO in topic for topic in topics)
