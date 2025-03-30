from enum import StrEnum


class Configuration(StrEnum):
    GLOBAL_TOPICS = "pytest_pubsub_global_topics"
    GLOBAL_DELETE = "pytest_pubsub_global_delete"
    PROJECT_ID = "pytest_pubsub_project_id"
    RUN_EMULATOR = "pytest_pubsub_run_emulator"


class MarkerConfiguration(StrEnum):
    """Configuration options for custom markers."""

    pubsub = "pubsub(topics=list, delete_after=bool, project_id=str)"


class HookConfiguration(StrEnum):
    """Configuration options for hooks."""
    ...
