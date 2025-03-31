from pytest import Pytester
from pytest_pubsub.config import Configuration, Defaults
from tests.enums import ProjectIds
from pytest_pubsub.pubsub.publisher import GCPPublisher


class TestPlugin:
    def test_global_create_topics(self, pytester: Pytester, publisher: GCPPublisher) -> None:
        pytester.makeini(f"""
        [pytest]
        {Configuration.GLOBAL_TOPICS} = 
            {ProjectIds.GLOBAL_TOPIC_CREATE_ONE}
            {ProjectIds.GLOBAL_TOPIC_CREATE_TWO}
        """)
        pytester.copy_example("test_plugin.py")
        result = pytester.runpytest("-k", "test_global_create_topics")
        result.assert_outcomes(passed=1)

        project_path = f"projects/{Defaults.PROJECT_ID}"
        found_topics = publisher.list_topics(request={"project": project_path})
        found_topics = [topic.name for topic in found_topics]

        topic_1 = publisher.topic_path(Defaults.PROJECT_ID, ProjectIds.GLOBAL_TOPIC_CREATE_ONE)
        topic_2 = publisher.topic_path(Defaults.PROJECT_ID, ProjectIds.GLOBAL_TOPIC_CREATE_TWO)

        assert topic_1 in found_topics
        assert topic_2 in found_topics

    def test_global_delete_topics(self, pytester: Pytester, publisher: GCPPublisher) -> None:
        pytester.makeini(f"""
        [pytest]
        {Configuration.GLOBAL_TOPICS} = 
            {ProjectIds.GLOBAL_TOPIC_DELETE_ONE}
            {ProjectIds.GLOBAL_TOPIC_DELETE_TWO}

        {Configuration.GLOBAL_DELETE} = True
        {Configuration.PROJECT_ID} = {ProjectIds.GLOBAL_DELETE}
        """)

        pytester.copy_example("test_plugin.py")
        result = pytester.runpytest("-k", "test_global_delete_topics")
        result.assert_outcomes(passed=1)

        project_path = f"projects/{ProjectIds.GLOBAL_DELETE}"
        found_topics = publisher.list_topics(request={"project": project_path})
        found_topics = [topic.name for topic in found_topics]

        assert len(found_topics) == 0