import uuid
from typing import AsyncGenerator
from typing import Generator

import pytest
import pytest_asyncio
from pulsar import Client  # type: ignore[import-untyped]
from pulsar import Consumer
from pulsar import Producer
from pulsar.asyncio import Client as AsyncClient  # type: ignore[import-untyped]
from pulsar.asyncio import Consumer as AsyncConsumer
from pulsar.asyncio import Producer as AsyncProducer
from pytest import Config
from pytest import FixtureRequest

from pytest_streaming.pulsar._models import TopicMeta
from pytest_streaming.pulsar.markers import PulsarMarker


@pytest.fixture
def streaming_pulsar_marker(request: FixtureRequest, pytestconfig: Config) -> PulsarMarker:
    """Usable PulsarMarker object

    Yields the base pulsar marker object that gives you access to the designated
    configurations for the individual test. See PulsarMarker specification.

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
        client.close()
        del client


@pytest_asyncio.fixture
async def async_streaming_pulsar_client(streaming_pulsar_marker: PulsarMarker) -> AsyncGenerator[AsyncClient, None]:
    """Async pulsar client using the service url configured for the given test.

    Does all of the necessary cleanup for you after the test concludes.

    Example:
        ```python
            from pulsar.asyncio import Client as AsyncClient

            @pytest.mark.pulsar(topics=["topic-a", "topic-b"])
            def test_pulsar_topics(async_streaming_pulsar_client: AsyncClient):
                assert isinstance(async_streaming_pulsar_client, AsyncClient)
        ```

    Returns:
        pulsar.asyncio.Client: async pulsar client from the base pulsar library
    """
    async_client = AsyncClient(service_url=streaming_pulsar_marker.service_url)
    try:
        yield async_client
    finally:
        await async_client.close()
        del async_client


@pytest.fixture
def streaming_pulsar_consumer(
    streaming_pulsar_client: Client, streaming_pulsar_marker: PulsarMarker
) -> Generator[Consumer, None]:
    """Raw pulsar consumer using the topics configured for the given test. Yields a unique subscription name each time.

    Does all of the necessary cleanup for you after the test concludes.

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
        consumer.close()
        del consumer


@pytest_asyncio.fixture
async def async_streaming_pulsar_consumer(
    async_streaming_pulsar_client: AsyncClient, streaming_pulsar_marker: PulsarMarker
) -> AsyncGenerator[AsyncConsumer, None]:
    """Async pulsar consumer using the topics configured for the given test. Yields a unique subscription name each time.

    Does all of the necessary cleanup for you after the test concludes.

    Example:
        ```python
            from pulsar.asyncio import Consumer as AsyncConsumer

            @pytest.mark.pulsar(topics=["topic-a", "topic-b"])
            def test_pulsar_topics(async_streaming_pulsar_consumer: AsyncConsumer):
                print(async_streaming_pulsar_consumer.subscription_name)
                msg = async_streaming_pulsar_consumer.receive()
        ```

    Returns:
        pulsar.asyncio.Consumer: async pulsar consumer from the base pulsar library
    """
    async_consumer = await async_streaming_pulsar_client.subscribe(
        topic=streaming_pulsar_marker.topics, subscription_name=str(uuid.uuid4())
    )
    try:
        yield async_consumer
    finally:
        await async_consumer.close()
        del async_consumer


@pytest.fixture
def streaming_pulsar_producers(
    streaming_pulsar_client: Client, streaming_pulsar_marker: PulsarMarker
) -> Generator[dict[str, Producer], None]:
    """Raw pulsar producer using the topics configured for the given test.

    Does all of the necessary cleanup for you after the test concludes.

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
            producer.close()
            del producer


@pytest_asyncio.fixture
async def async_streaming_pulsar_producers(
    async_streaming_pulsar_client: AsyncClient, streaming_pulsar_marker: PulsarMarker
) -> AsyncGenerator[dict[str, AsyncProducer], None]:
    """Async pulsar producer using the topics configured for the given test.

    Does all of the necessary cleanup for you after the test concludes.

    Example:
        ```python
            from pulsar.asyncio import Producer as AsyncProducer

            @pytest.mark.pulsar(topics=["topic-a", "topic-b"])
            def test_pulsar_topics(async_streaming_pulsar_producers: dict[str, AsyncProducer]):
                producer_a = async_streaming_pulsar_producers["topic-a"]
                producer_b = async_streaming_pulsar_producers["topic-b"]
                await producer_a.send(...)
                await producer_b.send(...)
        ```

    Returns:
        dict[topic.name, pulsar.asyncio.Producer]: async pulsar producers from the base pulsar library
    """

    # TODO: update to property w/ support for dynamic tenant/namespace
    topic_objs = [
        TopicMeta(
            topic_name=topic, tenant=streaming_pulsar_marker._tenant, namespace=streaming_pulsar_marker._namespace
        )
        for topic in streaming_pulsar_marker.topics
    ]

    async_producers = {
        topic_obj.short: await async_streaming_pulsar_client.create_producer(topic_obj.long) for topic_obj in topic_objs
    }

    try:
        yield async_producers
    finally:
        for _, producer in async_producers.items():
            await producer.close()
            del producer
