from enum import StrEnum

from pytest_streaming.config import Defaults


class ProjectIds(StrEnum):
    DEFAULT = Defaults.PROJECT_ID
    GLOBAL_DELETE = "pytest-streaming-pubsub-global-delete"

    # FIXME: these are topics not project ids
    PYTEST_PUBSUB = "pytest-streaming-pubsub"
    PYTEST_PUBSUB_DELETE = "pytest-streaming-pubsub-delete"
    PUBLISHER_PUBSUB_CREATE = "pytest-streaming-publisher-pubsub-create"
    PUBLISHER_PUBSUB_DELETE = "pytest-streaming-publisher-pubsub-delete"
    GLOBAL_TOPIC_CREATE_ONE = "pytest-streaming-pubsub-global-create-topic-1"
    GLOBAL_TOPIC_CREATE_TWO = "pytest-streaming-pubsub-global-create-topic-2"
    GLOBAL_TOPIC_DELETE_ONE = "pytest-streaming-pubsub-global-delete-topic-1"
    GLOBAL_TOPIC_DELETE_TWO = "pytest-streaming-pubsub-global-delete-topic-2"
