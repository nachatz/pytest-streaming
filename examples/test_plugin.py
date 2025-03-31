from google.cloud.pubsub_v1 import PublisherClient # type: ignore[import-untyped]
from pytest_pubsub.config import Defaults
from tests.enums import ProjectIds


class TestPlugin:
    def test_global_create_topics(self) -> None:
        publisher = PublisherClient()
        project_id = Defaults.PROJECT_ID
        project_path = f"projects/{project_id}"

        found_topics = publisher.list_topics(request={"project": project_path})
        found_topics = [topic.name for topic in found_topics]

        topic_1 = publisher.topic_path(project_id, ProjectIds.GLOBAL_TOPIC_CREATE_ONE)
        topic_2 = publisher.topic_path(project_id, ProjectIds.GLOBAL_TOPIC_CREATE_TWO)

        assert topic_1 in found_topics
        assert topic_2 in found_topics

    def test_global_delete_topics(self) -> None:
        publisher = PublisherClient()
        project_id = ProjectIds.GLOBAL_DELETE
        project_path = f"projects/{project_id}"

        found_topics = publisher.list_topics(request={"project": project_path})
        found_topics = [topic.name for topic in found_topics]

        topic_1 = publisher.topic_path(project_id, ProjectIds.GLOBAL_TOPIC_DELETE_ONE)
        topic_2 = publisher.topic_path(project_id, ProjectIds.GLOBAL_TOPIC_DELETE_TWO)

        assert len(found_topics) == 2
        assert topic_1 in found_topics
        assert topic_2 in found_topics