from contextlib import contextmanager
from typing import Generator

from pytest import Config
from pytest import FixtureRequest

from pytest_streaming.config import Configuration
from pytest_streaming.pubsub.publisher import GCPPublisher


@contextmanager
def pubsub_setup_marker(request: FixtureRequest, pytestconfig: Config) -> Generator[None, None, None]:
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
    project_id = override_project_id or pytestconfig.getini(Configuration.PUBSUB_PROJECT_ID)
    topics = marker.kwargs.get("topics", [])
    if not topics:
        raise ValueError("No topics specified for the pubsub marker")

    GCPPublisher().setup_testing_topics(project_id, topics)

    yield

    if delete_after:
        GCPPublisher().delete_testing_topics(project_id, topics)
