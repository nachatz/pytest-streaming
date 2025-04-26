from pytest import Pytester

from pytest_streaming.config import Configuration
from pytest_streaming.config import Defaults
from pytest_streaming.pubsub.publisher import GCPPublisher
from tests.pubsub.enums import PubsubProjectId
from tests.pubsub.enums import PubsubTopicName


class TestPubsubPlugin:
    def test_global_create_topics(self, pytester: Pytester, publisher: GCPPublisher) -> None:
        pytester.makeini(f"""
        [pytest]
        {Configuration.PUBSUB_GLOBAL_TOPICS} = 
            {PubsubTopicName.GLOBAL_TOPIC_CREATE_ONE}
            {PubsubTopicName.GLOBAL_TOPIC_CREATE_TWO}
        """)
        pytester.copy_example("test_pubsub_plugin.py")
        result = pytester.runpytest("-k", "test_pubsub_global_create_topics")
        result.assert_outcomes(passed=1)

        project_path = f"projects/{Defaults.PROJECT_ID}"
        found_topics = publisher.list_topics(request={"project": project_path})
        found_topics = [topic.name for topic in found_topics]

        topic_1 = publisher.topic_path(Defaults.PROJECT_ID, PubsubTopicName.GLOBAL_TOPIC_CREATE_ONE)
        topic_2 = publisher.topic_path(Defaults.PROJECT_ID, PubsubTopicName.GLOBAL_TOPIC_CREATE_TWO)

        assert topic_1 in found_topics
        assert topic_2 in found_topics

    def test_global_delete_topics(self, pytester: Pytester, publisher: GCPPublisher) -> None:
        pytester.makeini(f"""
        [pytest]
        {Configuration.PUBSUB_GLOBAL_TOPICS} = 
            {PubsubTopicName.GLOBAL_TOPIC_DELETE_ONE}
            {PubsubTopicName.GLOBAL_TOPIC_DELETE_TWO}

        {Configuration.PUBSUB_GLOBAL_DELETE} = True
        {Configuration.PUBSUB_PROJECT_ID} = {PubsubProjectId.GLOBAL_DELETE}
        """)

        pytester.copy_example("test_pubsub_plugin.py")
        result = pytester.runpytest("-k", "test_pubsub_global_delete_topics")
        result.assert_outcomes(passed=1)

        project_path = f"projects/{PubsubProjectId.GLOBAL_DELETE}"
        found_topics = publisher.list_topics(request={"project": project_path})
        found_topics = [topic.name for topic in found_topics]

        assert len(found_topics) == 0
