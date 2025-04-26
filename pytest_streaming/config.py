from enum import StrEnum


class Configuration(StrEnum):
    """Configuration options for pytest_streaming for
    pytest.ini file."""

    PUBSUB_GLOBAL_TOPICS = "pytest_streaming_pubsub_global_topics"
    PUBSUB_GLOBAL_DELETE = "pytest_streaming_pubsub_global_delete"
    PUBSUB_PROJECT_ID = "pytest_streaming_pubsub_project_id"
    PUBSUB_EMULATOR_ENABLED = "pytest_streaming_pubsub_emulator_enabled"


class Defaults(StrEnum):
    """Default values for pytest_streaming."""

    PROJECT_ID = "pytest-streaming"


class HookConfiguration(StrEnum): ...
