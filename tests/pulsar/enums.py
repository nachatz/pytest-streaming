from enum import StrEnum


class PulsarTopicName(StrEnum):
    """Topics used across example and source testing."""

    GLOBAL_TOPIC_CREATE_ONE = "pytest-streaming-pulsar-global-create-topic-1"
    GLOBAL_TOPIC_CREATE_TWO = "pytest-streaming-pulsar-global-create-topic-2"
    GLOBAL_TOPIC_DELETE_ONE = "pytest-streaming-pulsar-global-delete-topic-1"
    GLOBAL_TOPIC_DELETE_TWO = "pytest-streaming-pulsar-global-delete-topic-2"

    MARKER_TOPIC_CREATE_ONE = "pytest-streaming-pulsar-marker-create-topic-1"
    MARKER_TOPIC_CREATE_TWO = "pytest-streaming-pulsar-marker-create-topic-2"
    MARKER_TOPIC_DELETE_ONE = "pytest-streaming-pulsar-marker-delete-topic-1"
    MARKER_TOPIC_DELETE_TWO = "pytest-streaming-pulsar-marker-delete-topic-2"
