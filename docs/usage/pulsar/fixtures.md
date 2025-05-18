# Available Pulsar Fixtures

The plugin provides several fixtures to streamline the use of Apache Pulsar in your tests. These fixtures handle setup and teardown automatically, ensuring resources are managed efficiently and tests remain isolated.

## streaming_pulsar_marker

Yields a `PulsarMarker` object, which encapsulates all marker-based configuration for the current test. It provides access to the topics, service URL, admin URL, and other marker parameters as defined either in the test marker or in the global pytest configuration.

### Pulsar Marker Parameters

- `marker_name` (str): Name of the marker.
- `marker_description` (str): Description of the marker.
- `topics` (list[str]): A list of Pulsar topic names created.
- `delete_after` (bool): Whether or not topics are deleted after this test concludes.
- `service_url` (str): The Pulsar service URL.
- `admin_url` (str): The Pulsar admin URL.

**Usage Example:**

```python
from streaming.pulsar.markers import PulsarMarker

@pytest.mark.pulsar(topics=["topic-a", "topic-b"])
def test_pulsar_topics(streaming_pulsar_marker: PulsarMarker):
    assert streaming_pulsar_marker.topics == ["topic-a", "topic-b"]
```

## streaming_pulsar_client

Yields a raw Pulsar client, configured using the service URL from the current marker or global configuration. The client is automatically cleaned up after the test completes.

**Usage Example:**

```python
from pulsar import Client

@pytest.mark.pulsar(topics=["topic-a"])
def test_pulsar_client(streaming_pulsar_client: Client):
    assert isinstance(streaming_pulsar_client, Client)
```

## streaming_pulsar_consumer

Yields a Pulsar consumer, subscribed to the topics specified in the marker. Each consumer is given a unique subscription name for the test. Cleanup is handled automatically.

**Type:** `pulsar.Consumer`

**Usage Example:**

```python
from pulsar import Consumer

@pytest.mark.pulsar(topics=["topic-a"])
def test_pulsar_consumer(streaming_pulsar_consumer: Consumer):
    print(streaming_pulsar_consumer.subscription_name)
    msg = streaming_pulsar_consumer.receive()
```

## streaming_pulsar_producers

Yields a dictionary mapping topic names to Pulsar producer instances, one for each topic specified in the marker. All producers are cleaned up after the test.

**Type:** `dict[str, pulsar.Producer]`

**Usage Example:**

```python
from pulsar import Producer

@pytest.mark.pulsar(topics=["topic-a", "topic-b"])
def test_pulsar_producers(streaming_pulsar_producers: dict[str, Producer]):
    producer_a = streaming_pulsar_producers["topic-a"]
    producer_b = streaming_pulsar_producers["topic-b"]
    producer_a.send(...)
    producer_b.send(...)
```

These fixtures can be used independently or together, depending on the needs of your test. They abstract away the boilerplate of Pulsar client and resource management, allowing you to focus on your test logic.

## Full example

```python
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
```

If you're using these as objects in your codebase, you can simply mock them in-place:

```python
@pytest.mark.pulsar(topics=[PulsarTopicName.FIXTURE_MARKER_TOPIC_TWO])
def test_pulsar_producers_fixture(
    self, 
    streaming_pulsar_producers: dict[str, Producer], 
    streaming_pulsar_consumer: Consumer,
    your_client: MyCustomProducer,
    mocker: MockerFixture # from pytest
) -> None:
    mocker.patch.object(your_client, "producer", new=pulsar_producer)
```
