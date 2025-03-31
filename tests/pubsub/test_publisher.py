import pytest

from pytest_pubsub.pubsub.publisher import GCPPublisher
from tests.conftest import _TestProjectIds

class TestPublisher:

    @pytest.fixture
    def publisher(self) -> GCPPublisher:
        return GCPPublisher()
    
    def test_setup_pubsub_topics(self, publisher: GCPPublisher) -> None:
        project_id = _TestProjectIds.PUBLISHER_PUBSUB
        topics = ["topic1", "topic2"]
        publisher.setup_testing_topics(project_id, topics)

        for topic in topics:
            topic_path = publisher.topic_path(project_id, topic)
            assert topic_path in [t.name for t in publisher.list_topics(request={"project": project_id})]

        