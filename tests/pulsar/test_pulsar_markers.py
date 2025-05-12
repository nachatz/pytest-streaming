from pytest import Pytester

from pytest_streaming.config import Defaults
from pytest_streaming.pulsar.client import PulsarClientWrapper
from tests.pulsar.enums import PulsarTopicName


class TestPulsarMarkers:
    def test_pulsar_marker_topic_creation_base(self, pytester: Pytester, pulsar_client: PulsarClientWrapper) -> None:
        pytester.copy_example("test_pulsar_marker.py")
        result = pytester.runpytest("-k", "test_pulsar_marker_topic_creation_base")
        result.assert_outcomes(passed=1)

        # no auto delete by default
        topics = [PulsarTopicName.MARKER_TOPIC_CREATE_ONE, PulsarTopicName.MARKER_TOPIC_CREATE_TWO]
        found_topics = pulsar_client._get_topics(tenant=Defaults.PULSAR_TENANT, namespace=Defaults.PULSAR_NAMESPACE)
        for topic in topics:
            assert any(topic in found_topic for found_topic in found_topics)

    def test_pulsar_marker_topic_creation_autodelete(
        self, pytester: Pytester, pulsar_client: PulsarClientWrapper
    ) -> None:
        pytester.copy_example("test_pulsar_marker.py")
        result = pytester.runpytest("-k", "test_pulsar_marker_topic_creation_autodelete")
        result.assert_outcomes(passed=1)

        # ensure auto delete
        topics = [PulsarTopicName.MARKER_TOPIC_DELETE_ONE, PulsarTopicName.MARKER_TOPIC_DELETE_TWO]
        found_topics = pulsar_client._get_topics(tenant=Defaults.PULSAR_TENANT, namespace=Defaults.PULSAR_NAMESPACE)
        for topic in topics:
            assert all(topic not in found_topic for found_topic in found_topics)

    def test_pulsar_marker_topic_no_topics(self, pytester: Pytester) -> None:
        pytester.copy_example("test_pulsar_marker.py")
        result = pytester.runpytest("-k", "test_pulsar_marker_topic_no_topics")
        result.assert_outcomes(errors=1)
