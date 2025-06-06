from pytest import Pytester

from pytest_streaming.pubsub.publisher import GCPPublisher
from tests.pubsub.enums import PubsubProjectId


class TestPubsubMarkers:
    def test_pubsub_marker_topic_creation_base(self, pytester: Pytester) -> None:
        pytester.copy_example("test_pubsub_marker.py")
        result = pytester.runpytest("-k", "test_pubsub_marker_topic_creation_base")
        result.assert_outcomes(passed=1)

    def test_pubsub_marker_topic_creation_project_id(self, pytester: Pytester) -> None:
        pytester.copy_example("test_pubsub_marker.py")
        result = pytester.runpytest("-k", "test_pubsub_marker_topic_creation_project_id")
        result.assert_outcomes(passed=1)

    def test_pubsub_marker_topic_creation_autodelete(self, pytester: Pytester, gcp_publisher: GCPPublisher) -> None:
        pytester.copy_example("test_pubsub_marker.py")
        result = pytester.runpytest("-k", "test_pubsub_marker_topic_creation_autodelete")
        result.assert_outcomes(passed=1)

        project_id = PubsubProjectId.FIXTURE_DELETE
        project_path = f"projects/{project_id}"
        found_topics = gcp_publisher.list_topics(request={"project": project_path})
        found_topics = [topic.name for topic in found_topics]
        assert len(list(found_topics)) == 0, "Topics were not deleted after test completion"

    def test_pubsub_marker_no_topics(self, pytester: Pytester) -> None:
        pytester.copy_example("test_pubsub_marker.py")
        result = pytester.runpytest("-k", "test_pubsub_marker_no_topics")
        result.assert_outcomes(errors=3)
        assert "No topics specified" in result.stdout.str()
