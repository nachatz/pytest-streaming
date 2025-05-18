import pytest
from httpx import URL
from pytest_mock import MockerFixture

from pytest_streaming.config import Defaults
from pytest_streaming.pulsar._models import TopicMeta
from pytest_streaming.pulsar.client import AdminClient
from pytest_streaming.pulsar.client import PulsarClientWrapper
from tests.pulsar.enums import PulsarTopicName


class TestAdminClient:
    def test_admin_client_setup(self, pulsar_admin_client: AdminClient) -> None:
        assert pulsar_admin_client.USER_AGENT == "pytest-streaming"
        assert pulsar_admin_client.CONTENT_TYPE == "application/json"
        assert pulsar_admin_client.CONNECTION_TIMEOUT_SECONDS == 5
        assert pulsar_admin_client.base_url == URL(f"{Defaults.PULSAR_ADMIN_URL.value.rstrip('/')}/admin/v2/")

    @pytest.mark.vcr()
    def test_get_topics(self, pulsar_admin_client: AdminClient) -> None:
        topics = pulsar_admin_client.get_topics(
            tenant=Defaults.PULSAR_TENANT.value, namespace=Defaults.PULSAR_NAMESPACE.value
        )
        assert isinstance(topics, list)

    @pytest.mark.vcr()
    def test_delete_topic(
        self,
        pulsar_admin_client: AdminClient,
        pulsar_client: PulsarClientWrapper,
    ) -> None:
        topic = PulsarTopicName.ADMIN_CLIENT_TOPIC_CREATE_ONE
        topic_meta = TopicMeta(
            topic_name=topic, tenant=Defaults.PULSAR_TENANT.value, namespace=Defaults.PULSAR_NAMESPACE.value
        )
        pulsar_client._create_topic(topic=topic_meta)

        found_topics = pulsar_admin_client.get_topics(
            tenant=Defaults.PULSAR_TENANT.value, namespace=Defaults.PULSAR_NAMESPACE.value
        )
        assert any(topic in found_topic for found_topic in found_topics)

        topic_meta = TopicMeta(
            topic_name=topic, tenant=Defaults.PULSAR_TENANT.value, namespace=Defaults.PULSAR_NAMESPACE.value
        )
        pulsar_admin_client.delete_topic(topic=topic_meta)

        found_topics = pulsar_admin_client.get_topics(
            tenant=Defaults.PULSAR_TENANT.value, namespace=Defaults.PULSAR_NAMESPACE.value
        )
        assert all(topic not in found_topic for found_topic in found_topics)

    @pytest.mark.vcr()
    def test_delete_topic_not_real(self, pulsar_admin_client: AdminClient) -> None:
        topic_meta = TopicMeta(
            topic_name="not real", tenant=Defaults.PULSAR_TENANT.value, namespace=Defaults.PULSAR_NAMESPACE.value
        )
        pulsar_admin_client.delete_topic(topic=topic_meta)


class TestPulsarClientWrapper:
    def test_setup_testing_topics(self, pulsar_client: PulsarClientWrapper, mocker: MockerFixture) -> None:
        topics = ["fake", "topics"]

        delete_topic_mock = mocker.patch.object(
            pulsar_client.client, AdminClient.delete_topic.__name__, return_value=None
        )

        create_topic_mock = mocker.patch.object(
            pulsar_client, PulsarClientWrapper._create_topic.__name__, return_value=None
        )

        topic_meta = [
            TopicMeta(topic_name=topic, tenant=Defaults.PULSAR_TENANT.value, namespace=Defaults.PULSAR_NAMESPACE.value)
            for topic in topics
        ]
        pulsar_client.setup_testing_topics(topics=topic_meta)
        assert delete_topic_mock.call_count == 2
        assert create_topic_mock.call_count == 2

    def test_setup_testing_topics_failed_delete(
        self, pulsar_client: PulsarClientWrapper, mocker: MockerFixture
    ) -> None:
        topics = ["fake", "topics"]

        mocker.patch.object(pulsar_client.client, AdminClient.delete_topic.__name__, return_value=None)

        mocker.patch.object(pulsar_client.client, AdminClient.get_topics.__name__, return_value=["fake"])

        mocker.patch.object(pulsar_client, PulsarClientWrapper._create_topic.__name__, return_value=None)

        with pytest.raises(ValueError):
            topic_meta = [
                TopicMeta(
                    topic_name=topic, tenant=Defaults.PULSAR_TENANT.value, namespace=Defaults.PULSAR_NAMESPACE.value
                )
                for topic in topics
            ]
            pulsar_client.setup_testing_topics(topics=topic_meta)

    def test_delete_testing_topics(self, pulsar_client: PulsarClientWrapper, mocker: MockerFixture) -> None:
        topics = ["fake", "topics"]

        delete_topic_mock = mocker.patch.object(
            pulsar_client.client, AdminClient.delete_topic.__name__, return_value=None
        )

        topic_meta = [
            TopicMeta(topic_name=topic, tenant=Defaults.PULSAR_TENANT.value, namespace=Defaults.PULSAR_NAMESPACE.value)
            for topic in topics
        ]
        pulsar_client.delete_testing_topics(topics=topic_meta)
        assert delete_topic_mock.call_count == 2
