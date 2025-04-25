from enum import StrEnum


class Configuration(StrEnum):
    """Configuration options for pytest_streaming."""

    PUBSUB_GLOBAL_TOPICS = "pytest_streaming_pubsub_global_topics"
    PUBSUB_GLOBAL_DELETE = "pytest_streaming_pubsub_global_delete"
    PUBSUB_PROJECT_ID = "pytest_streaming_pubsub_project_id"


class Defaults(StrEnum):
    """Default values for pytest_streaming."""

    PROJECT_ID = "pytest-streaming"


class MarkerConfiguration(StrEnum):
    """Configuration options for custom markers."""

    pubsub = "pubsub(topics=list, delete_after=bool, project_id=str)"


class HookConfiguration(StrEnum):
    """Configuration options for hooks."""

    ...
