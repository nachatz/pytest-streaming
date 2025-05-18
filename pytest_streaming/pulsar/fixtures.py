import uuid
from typing import Generator

import pytest
from pulsar import Client  # type: ignore[import-untyped]
from pulsar import Consumer
from pulsar import Producer
from pytest import Config
from pytest import FixtureRequest

from pytest_streaming.pulsar._models import TopicMeta
from pytest_streaming.pulsar.markers import PulsarMarker


@pytest.fixture
def streaming_pulsar_marker(request: FixtureRequest, pytestconfig: Config) -> PulsarMarker:
    """Usable PulsarMarker object

    Yields the base pulsar marker object that gives you access to the designated
    configurations for the individual test

    Args:
        request (FixtureRequest -- auto requested): pytest fixture request
        pytestconfig (Config -- auto requested): pytest config context object

    Example:
        ```python
            from streaming.pulsar.markers import PulsarMarker

            @pytest.mark.pulsar(topics=["topic-a", "topic-b"])
            def test_pulsar_topics(streaming_pulsar_marker: PulsarMarker):
                assert PulsarMarker.topics == ["topic-a", "topic-b"]
        ```

    Returns:
        PulsarMarker: object with all of the defined user configurations

    """
    return PulsarMarker(config=pytestconfig, request=request)


@pytest.fixture
def streaming_pulsar_client(streaming_pulsar_marker: PulsarMarker) -> Generator[Client, None]:
    """Raw pulsar client using the service url configured for the given test.

    Does all of the necessary cleanup for you after the test concludes.

    Args:
        streaming_pulsar_marker (PulsarMarker -- auto requested): pulsar marker used in the scope of this test

    Example:
        ```python
            from pulsar import Client

            @pytest.mark.pulsar(topics=["topic-a", "topic-b"])
            def test_pulsar_topics(streaming_pulsar_client: Client):
                assert isinstance(streaming_pulsar_client, Client)
        ```

    Returns:
        pulsar.Client: raw pulsar client from the base pulsar library
    """
    client = Client(service_url=streaming_pulsar_marker.service_url)
    try:
        yield client
    finally:
        del client


@pytest.fixture
def streaming_pulsar_consumer(
    streaming_pulsar_client: Client, streaming_pulsar_marker: PulsarMarker
) -> Generator[Consumer, None]:
    """Raw pulsar consumer using the topics configured for the given test. Yields a unique subscription name each time.

    Does all of the necessary cleanup for you after the test concludes.

    Args:
        streaming_pulsar_marker (PulsarMarker -- auto requested): pulsar marker used in the scope of this test
        streaming_pulsar_client (Client -- auto requested): raw pulsar client from the base pulsar library

    Example:
        ```python
            from pulsar import Consumer

            @pytest.mark.pulsar(topics=["topic-a", "topic-b"])
            def test_pulsar_topics(streaming_pulsar_consumer: Consumer):
                print(streaming_pulsar_consumer.subscription_name)
                msg = streaming_pulsar_consumer.receive()
        ```

    Returns:
        pulsar.Consumer: raw pulsar consumer from the base pulsar library
    """
    consumer = streaming_pulsar_client.subscribe(
        topic=streaming_pulsar_marker.topics, subscription_name=str(uuid.uuid4())
    )
    try:
        yield consumer
    finally:
        del consumer


@pytest.fixture
def streaming_pulsar_producers(
    streaming_pulsar_client: Client, streaming_pulsar_marker: PulsarMarker
) -> Generator[dict[str, Producer], None]:
    """Raw pulsar producer using the topics configured for the given test.

    Does all of the necessary cleanup for you after the test concludes.

    Args:
        streaming_pulsar_marker (PulsarMarker -- auto requested): pulsar marker used in the scope of this test
        streaming_pulsar_client (Client -- auto requested): raw pulsar client from the base pulsar library

    Example:
        ```python
            from pulsar import Producer

            @pytest.mark.pulsar(topics=["topic-a", "topic-b"])
            def test_pulsar_topics(streaming_pulsar_producers: dict[str, Producer]):
                producer_a = streaming_pulsar_producers["topic-a"]
                producer_b = streaming_pulsar_producers["topic-b"]
                producer_a.send(...)
                producer_b.send(...)
        ```

    Returns:
        dict[topic.name, pulsar.Producer]: raw pulsar producers from the base pulsar library
    """

    # TODO: update to property w/ support for dynamic tenant/namespace
    topic_objs = [
        TopicMeta(
            topic_name=topic, tenant=streaming_pulsar_marker._tenant, namespace=streaming_pulsar_marker._namespace
        )
        for topic in streaming_pulsar_marker.topics
    ]

    producers = {topic_obj.short: streaming_pulsar_client.create_producer(topic_obj.long) for topic_obj in topic_objs}

    try:
        yield producers
    finally:
        for _, producer in producers.items():
            del producer
