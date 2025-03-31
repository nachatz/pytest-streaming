import pytest

from pytest import FixtureRequest
from google.cloud.pubsub_v1 import PublisherClient  # type: ignore

from pytest_pubsub.config import Defaults
from tests.conftest import ProjectIds


class TestPubsubMarker:
    @pytest.mark.pubsub(topics=["test-topic1", "test-topic2"])
    def test_pubsub_marker_topic_creation_base(self, request: FixtureRequest) -> None:
        marker = request.node.get_closest_marker("pubsub")
        topics = marker.kwargs["topics"]

        project_id = Defaults.PROJECT_ID
        publisher = PublisherClient()
        project_path = f"projects/{project_id}"

        found_topics = publisher.list_topics(request={"project": project_path})
        found_topics = [topic.name for topic in found_topics]
        path_1 = publisher.topic_path(project_id, topics[0])
        path_2 = publisher.topic_path(project_id, topics[1])

        assert len(topics) == 2 == len(found_topics)
        assert path_1 in found_topics
        assert path_2 in found_topics
        assert project_id == Defaults.PROJECT_ID

    @pytest.mark.pubsub(
        topics=["test-topic1", "test-topic2"], 
        project_id=ProjectIds.PYTEST_PUBSUB
    )
    def test_pubsub_marker_topic_creation_project_id(self, request: FixtureRequest) -> None:
        marker = request.node.get_closest_marker("pubsub")
        topics = marker.kwargs["topics"]
        project_id = marker.kwargs["project_id"]

        publisher = PublisherClient()
        project_path = f"projects/{project_id}"

        found_topics = publisher.list_topics(request={"project": project_path})
        found_topics = [topic.name for topic in found_topics]
        path_1 = publisher.topic_path(project_id, topics[0])
        path_2 = publisher.topic_path(project_id, topics[1])

        assert len(topics) == 2 == len(found_topics)
        assert path_1 in found_topics
        assert path_2 in found_topics
        assert project_id == ProjectIds.PYTEST_PUBSUB

    @pytest.mark.pubsub(
        topics=["test-topic1", "test-topic2"], 
        delete_after=True, 
        project_id=ProjectIds.PYTEST_PUBSUB_DELETE
    )
    def test_pubsub_marker_topic_creation_autodelete(self, request: FixtureRequest) -> None:
        marker = request.node.get_closest_marker("pubsub")
        topics = marker.kwargs["topics"]
        project_id = marker.kwargs["project_id"]

        publisher = PublisherClient()
        project_path = f"projects/{project_id}"

        found_topics = publisher.list_topics(request={"project": project_path})
        found_topics = [topic.name for topic in found_topics]
        path_1 = publisher.topic_path(project_id, topics[0])
        path_2 = publisher.topic_path(project_id, topics[1])

        assert len(topics) == 2 == len(found_topics)
        assert path_1 in found_topics
        assert path_2 in found_topics
        assert project_id == ProjectIds.PYTEST_PUBSUB_DELETE
        assert marker.kwargs["delete_after"] is True

    @pytest.mark.pubsub
    def test_pubsub_marker_no_topics(self) -> None:
        assert True

    @pytest.mark.pubsub(topics=[])
    def test_pubsub_marker_no_topics_empty(self) -> None:
        assert True

    @pytest.mark.pubsub(project_id="abc", delete_after=True)
    def test_pubsub_marker_no_topics_params(self) -> None:
        assert True