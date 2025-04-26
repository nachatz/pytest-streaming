from pytest_streaming.pubsub.publisher import GCPPublisher
from tests.pubsub.enums import PubsubProjectId


class TestPublisher:
    def test_pubsub_topics_create(self, publisher: GCPPublisher) -> None:
        project_id = PubsubProjectId.PUBLISHER_CREATE
        topics = ["topic1", "topic2"]
        project_path = f"projects/{project_id}"

        publisher.setup_testing_topics(project_id, topics)
        for topic in topics:
            topic_path = publisher.topic_path(project_id, topic)
            assert topic_path in [t.name for t in publisher.list_topics(request={"project": project_path})]

    def test_pubsub_topics_delete(self, publisher: GCPPublisher) -> None:
        project_id = PubsubProjectId.PUBLISHER_DELETE
        topics = ["topic1", "topic2"]
        project_path = f"projects/{project_id}"

        publisher.setup_testing_topics(project_id, topics)
        for topic in topics:
            topic_path = publisher.topic_path(project_id, topic)
            assert topic_path in [t.name for t in publisher.list_topics(request={"project": project_path})]

        publisher.delete_testing_topics(project_id, topics)
        for topic in topics:
            topic_path = publisher.topic_path(project_id, topic)
            assert topic_path not in [t.name for t in publisher.list_topics(request={"project": project_path})]
