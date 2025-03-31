import pytest
from google.api_core.exceptions import NotFound
from pytest import Config

from pytest_pubsub.pubsub.publisher import GCPPublisher
from tests.enums import ProjectIds

pytest_plugins = ["pytester"]


@pytest.fixture(scope="session", autouse=True)
def plugin_was_loaded(pytestconfig: Config) -> None:
    """Ensures the pytest-pubsub plugin is loaded."""
    assert pytestconfig.pluginmanager.hasplugin("pytest_pubsub")


@pytest.fixture(scope="session")
def project_ids() -> list[str]:
    """Returns a list of project IDs used in tests sourced
    from ProjectIds enum."""
    return [member.value for member in ProjectIds]


@pytest.fixture(scope="session")
def publisher() -> GCPPublisher:
    return GCPPublisher()


@pytest.fixture(scope="session", autouse=True)
def destroy_topics(project_ids: list[str], publisher: GCPPublisher) -> None:
    """Ensures the pubsub topics are cleansed prior to each test.

    Args:
        project_ids (fixture: list[str]): List of project IDs to clean up.
        publisher (fixture: GCPPublisher): The GCPPublisher instance to use for cleanup.
    """
    for project_id in project_ids:
        project_path = f"projects/{project_id}"
        found_topics = publisher.list_topics(request={"project": project_path})
        found_topics = [topic.name for topic in found_topics]

        for topic in found_topics:
            try:
                publisher.delete_topic(topic=topic)
            except NotFound:
                ...
