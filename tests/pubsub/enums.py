from enum import StrEnum

from pytest_streaming.config import Defaults


class PubsubProjectId(StrEnum):
    DEFAULT = Defaults.PROJECT_ID.value
    GLOBAL_DELETE = "pytest-streaming-pubsub-global-delete"

    FIXTURE = "pytest-streaming-fixture-pubsub"
    FIXTURE_DELETE = "pytest-streaming-fixture-pubsub-delete"
    PUBLISHER_CREATE = "pytest-streaming-publisher-pubsub-create"
    PUBLISHER_CREATE_CLEAN = "pytest-streaming-publisher-pubsub-create-clean"
    PUBLISHER_DELETE = "pytest-streaming-publisher-pubsub-delete"


class PubsubTopicName(StrEnum):
    GLOBAL_TOPIC_CREATE_ONE = "pytest-streaming-pubsub-global-create-topic-1"
    GLOBAL_TOPIC_CREATE_TWO = "pytest-streaming-pubsub-global-create-topic-2"
    GLOBAL_TOPIC_DELETE_ONE = "pytest-streaming-pubsub-global-delete-topic-1"
    GLOBAL_TOPIC_DELETE_TWO = "pytest-streaming-pubsub-global-delete-topic-2"
