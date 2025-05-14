from enum import Enum
from enum import StrEnum


class Configuration(StrEnum):
    """Configuration options for pytest_streaming for
    pytest.ini file."""

    # PubSub
    PUBSUB_GLOBAL_TOPICS = "pytest_streaming_pubsub_global_topics"
    PUBSUB_GLOBAL_DELETE = "pytest_streaming_pubsub_global_delete"
    PUBSUB_PROJECT_ID = "pytest_streaming_pubsub_project_id"
    PUBSUB_EMULATOR_ENABLED = "pytest_streaming_pubsub_emulator_enabled"

    # Pulsar
    PULSAR_GLOBAL_TOPICS = "pytest_streaming_pulsar_global_topics"
    PULSAR_GLOBAL_DELETE = "pytest_streaming_pulsar_global_delete"
    PULSAR_SERVICE_URL = "pytest_streaming_pulsar_service_url"
    PULSAR_ADMIN_URL = "pytest_streaming_pulsar_admin_url"
    PULSAR_TENANT = "pytest_streaming_pulsar_tenant"
    PULSAR_NAMESPACE = "pytest_streaming_pulsar_namespace"


class Defaults(Enum):
    """Default values for pytest_streaming."""

    # PubSub
    PROJECT_ID = "pytest-streaming"
    PUBSUB_EMULATOR_ENABLED = True
    PUBSUB_GLOBAL_DELETE = False

    # Pulsar
    PULSAR_SERVICE_URL = "pulsar://localhost:6650"
    PULSAR_ADMIN_URL = "http://localhost:8080"
    PULSAR_TENANT = "public"
    PULSAR_NAMESPACE = "default"
    PULSAR_AUTO_DELETE = False


class HookConfiguration(StrEnum): ...
