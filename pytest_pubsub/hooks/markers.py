import pytest

from pytest import FixtureRequest, Config
from typing import Generator

from pytest_pubsub.pubsub.publisher import GCPPublisher
from pytest_pubsub.config import Configuration


@pytest.fixture(autouse=True)
def _pubsub_setup(request: FixtureRequest, pytestconfig: Config) -> Generator[None, None, None]:
    """Creates and optionally deletes Pub/Sub topics for tests with the pubsub marker.

    Args:
        request: pytest fixture request object
        pytestconfig: pytest config object
    """
    marker = request.node.get_closest_marker("pubsub")
    if marker is None:
        yield
        return

    delete_after = marker.kwargs.get("delete_after", False)
    override_project_id = marker.kwargs.get("project_id", None)
    project_id = override_project_id or pytestconfig.getini(Configuration.PROJECT_ID)
    topics = marker.kwargs.get("topics", [])
    if not topics:
        raise ValueError("No topics specified for the pubsub marker")

    GCPPublisher().setup_testing_topics(project_id, topics)

    yield

    if delete_after:
        GCPPublisher().delete_testing_topics(project_id, topics)
