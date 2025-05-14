import pytest
from _pytest.nodes import Node
from google.cloud.pubsub_v1 import PublisherClient  # type: ignore
from pytest import FixtureRequest
from pytest import Mark

from pytest_streaming.config import Defaults
from tests.pubsub.enums import PubsubProjectId


class TestPubsubMarker:
    @pytest.fixture
    def publisher(self) -> PublisherClient:
        return PublisherClient()

    @pytest.mark.pubsub(topics=["test-topic1", "test-topic2"])
    def test_pubsub_marker_topic_creation_base(self, request: FixtureRequest, publisher: PublisherClient) -> None:
        node: Node = request.node
        marker: Mark = node.get_closest_marker("pubsub")  # type: ignore
        topics = marker.kwargs["topics"]

        project_id = Defaults.PROJECT_ID.value
        project_path = f"projects/{project_id}"

        found_topics = publisher.list_topics(request={"project": project_path})
        found_topics = [topic.name for topic in found_topics]
        path_1 = publisher.topic_path(project_id, topics[0])
        path_2 = publisher.topic_path(project_id, topics[1])

        assert path_1 in found_topics
        assert path_2 in found_topics
        assert project_id == Defaults.PROJECT_ID.value

    @pytest.mark.pubsub(topics=["test-topic1", "test-topic2"], project_id=PubsubProjectId.FIXTURE)
    def test_pubsub_marker_topic_creation_project_id(self, request: FixtureRequest, publisher: PublisherClient) -> None:
        node: Node = request.node
        marker: Mark = node.get_closest_marker("pubsub")  # type: ignore
        topics = marker.kwargs["topics"]
        project_id = marker.kwargs["project_id"]
        project_path = f"projects/{project_id}"

        found_topics = publisher.list_topics(request={"project": project_path})
        found_topics = [topic.name for topic in found_topics]
        path_1 = publisher.topic_path(project_id, topics[0])
        path_2 = publisher.topic_path(project_id, topics[1])

        assert len(topics) == 2 == len(found_topics)
        assert path_1 in found_topics
        assert path_2 in found_topics
        assert project_id == PubsubProjectId.FIXTURE

    @pytest.mark.pubsub(
        topics=["test-topic1", "test-topic2"], delete_after=True, project_id=PubsubProjectId.FIXTURE_DELETE
    )
    def test_pubsub_marker_topic_creation_autodelete(self, request: FixtureRequest, publisher: PublisherClient) -> None:
        node: Node = request.node
        marker: Mark = node.get_closest_marker("pubsub")  # type: ignore
        topics = marker.kwargs["topics"]
        project_id = marker.kwargs["project_id"]

        project_path = f"projects/{project_id}"

        found_topics = publisher.list_topics(request={"project": project_path})
        found_topics = [topic.name for topic in found_topics]
        path_1 = publisher.topic_path(project_id, topics[0])
        path_2 = publisher.topic_path(project_id, topics[1])

        assert len(topics) == 2 == len(found_topics)
        assert path_1 in found_topics
        assert path_2 in found_topics
        assert project_id == PubsubProjectId.FIXTURE_DELETE
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
