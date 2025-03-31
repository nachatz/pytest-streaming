from enum import StrEnum
from pytest_pubsub.config import Defaults


class ProjectIds(StrEnum):
    DEFAULT = Defaults.PROJECT_ID
    GLOBAL_DELETE = "pytest-pubsub-global-delete"

    # FIXME: these are topics not project ids
    PYTEST_PUBSUB = "pytest-pubsub"
    PYTEST_PUBSUB_DELETE = "pytest-pubsub-delete"
    PUBLISHER_PUBSUB_CREATE = "pytest-publisher-pubsub-create"
    PUBLISHER_PUBSUB_DELETE = "pytest-publisher-pubsub-delete"
    GLOBAL_TOPIC_CREATE_ONE = "pytest-pubsub-global-create-topic-1"
    GLOBAL_TOPIC_CREATE_TWO = "pytest-pubsub-global-create-topic-2"
    GLOBAL_TOPIC_DELETE_ONE = "pytest-pubsub-global-delete-topic-1"
    GLOBAL_TOPIC_DELETE_TWO = "pytest-pubsub-global-delete-topic-2"
