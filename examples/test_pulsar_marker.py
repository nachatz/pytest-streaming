import pytest
from _pytest.nodes import Node
from pytest import FixtureRequest
from pytest import Mark

from pytest_streaming.config import Defaults
from pytest_streaming.pulsar.client import PulsarClientWrapper
from tests.pulsar.enums import PulsarTopicName
from tests.settings import PulsarTestSettings


class TestPulsarMarker:
    @pytest.fixture()
    def settings(self) -> PulsarTestSettings:
        return PulsarTestSettings()

    @pytest.fixture()
    def pulsar_client(self, settings: PulsarTestSettings) -> PulsarClientWrapper:
        return PulsarClientWrapper(settings.service_url, settings.admin_url)

    @pytest.mark.pulsar(topics=[PulsarTopicName.MARKER_TOPIC_CREATE_ONE, PulsarTopicName.MARKER_TOPIC_CREATE_TWO])
    def test_pulsar_marker_topic_creation_base(
        self, pulsar_client: PulsarClientWrapper, request: FixtureRequest
    ) -> None:
        node: Node = request.node
        marker: Mark = node.get_closest_marker("pulsar")  # type: ignore
        topics: list[str] = marker.kwargs["topics"]

        found_topics: list[str] = pulsar_client.client.get_topics(
            tenant=Defaults.PULSAR_TENANT.value, namespace=Defaults.PULSAR_NAMESPACE.value
        )
        for topic in topics:
            assert any(topic in found_topic for found_topic in found_topics)

    @pytest.mark.pulsar(
        topics=[PulsarTopicName.MARKER_TOPIC_DELETE_ONE, PulsarTopicName.MARKER_TOPIC_DELETE_TWO], delete_after=True
    )
    def test_pulsar_marker_topic_creation_autodelete(
        self, pulsar_client: PulsarClientWrapper, request: FixtureRequest
    ) -> None:
        node: Node = request.node
        marker: Mark = node.get_closest_marker("pulsar")  # type: ignore
        topics: list[str] = marker.kwargs["topics"]

        found_topics: list[str] = pulsar_client.client.get_topics(
            tenant=Defaults.PULSAR_TENANT.value, namespace=Defaults.PULSAR_NAMESPACE.value
        )
        for topic in topics:
            assert any(topic in found_topic for found_topic in found_topics)

    @pytest.mark.pulsar(delete_after=True)
    def test_pulsar_marker_topic_no_topics(self) -> None:
        assert True
