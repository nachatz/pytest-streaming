import pytest
from pytest import MonkeyPatch

from pytest_streaming.pubsub.publisher import GCPPublisher
from tests.pubsub.enums import PubsubProjectId


class TestPubsubPublisher:
    def test_pubsub_topics_create(self, publisher: GCPPublisher) -> None:
        project_id = PubsubProjectId.PUBLISHER_CREATE
        topics = ["topic1", "topic2"]
        project_path = f"projects/{project_id}"

        publisher.setup_testing_topics(project_id, topics)
        for topic in topics:
            topic_path = publisher.topic_path(project_id, topic)
            assert topic_path in [t.name for t in publisher.list_topics(request={"project": project_path})]

    def test_pubsub_topics_create_clean(self, publisher: GCPPublisher) -> None:
        project_id = PubsubProjectId.PUBLISHER_CREATE_CLEAN
        topic = "topic1"
        project_path = f"projects/{project_id}"

        topic_path = publisher.topic_path(project=project_id, topic=topic)
        publisher.delete_testing_topics(project_id, [topic])

        publisher.create_topic(name=topic_path)

        publisher.setup_testing_topics(project_id, [topic])
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

    def test_emulator_enabled_true(self, publisher: GCPPublisher, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv("PUBSUB_EMULATOR_HOST", "localhost:8085")
        assert publisher.emulator_enabled is True

    def test_emulator_enabled_false(self, publisher: GCPPublisher, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv("PUBSUB_EMULATOR_HOST", "")
        assert publisher.emulator_enabled is False

    def test_emulator_enabled_topic_creation(self, publisher: GCPPublisher, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv("PUBSUB_EMULATOR_HOST", "")
        with pytest.raises(EnvironmentError):
            publisher.setup_testing_topics(project_id="test", topics=["topic1", "topic2"])

    def test_emulator_enabled_topic_deletion(self, publisher: GCPPublisher, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv("PUBSUB_EMULATOR_HOST", "")
        with pytest.raises(EnvironmentError):
            publisher.delete_testing_topics(project_id="test", topics=["topic1", "topic2"])
