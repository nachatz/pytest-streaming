import pytest
from pulsar import Client  # type: ignore[import-untyped]
from pulsar import Consumer
from pulsar import Producer

from pytest_streaming.pulsar.markers import PulsarMarker
from tests.pulsar.enums import PulsarTopicName


class TestPulsarFixture:
    @pytest.mark.pulsar(
        topics=[PulsarTopicName.FIXTURE_MARKER_TOPIC_ONE, PulsarTopicName.FIXTURE_MARKER_TOPIC_TWO], delete_after=True
    )
    def test_pulsar_marker_fixture(self, streaming_pulsar_marker: PulsarMarker) -> None:
        assert streaming_pulsar_marker.topics == [
            PulsarTopicName.FIXTURE_MARKER_TOPIC_ONE,
            PulsarTopicName.FIXTURE_MARKER_TOPIC_TWO,
        ]
        assert streaming_pulsar_marker.delete_after

    @pytest.mark.pulsar(topics=[PulsarTopicName.FIXTURE_MARKER_TOPIC_ONE])
    def test_pulsar_client_fixture(self, streaming_pulsar_client: Client) -> None:
        assert isinstance(streaming_pulsar_client, Client)

    @pytest.mark.pulsar(topics=[PulsarTopicName.FIXTURE_MARKER_TOPIC_ONE])
    def test_pulsar_consumer_fixture(
        self, streaming_pulsar_client: Client, streaming_pulsar_consumer: Consumer
    ) -> None:
        payload = b"test"
        producer = streaming_pulsar_client.create_producer(topic=PulsarTopicName.FIXTURE_MARKER_TOPIC_ONE)
        producer.send(payload)

        msg = streaming_pulsar_consumer.receive()
        assert isinstance(streaming_pulsar_consumer, Consumer)
        assert msg.data() == payload

    @pytest.mark.pulsar(topics=[PulsarTopicName.FIXTURE_MARKER_TOPIC_TWO])
    def test_pulsar_producers_fixture(
        self, streaming_pulsar_producers: dict[str, Producer], streaming_pulsar_consumer: Consumer
    ) -> None:
        payload = b"test"
        producer = streaming_pulsar_producers[PulsarTopicName.FIXTURE_MARKER_TOPIC_TWO]
        producer.send(payload)

        msg = streaming_pulsar_consumer.receive()
        assert isinstance(producer, Producer)
        assert len(streaming_pulsar_producers) == 1
        assert set(streaming_pulsar_producers) == {PulsarTopicName.FIXTURE_MARKER_TOPIC_TWO}
        assert msg.data() == payload
