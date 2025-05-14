from pytest import Pytester

from pytest_streaming.config import Configuration
from pytest_streaming.config import Defaults
from pytest_streaming.pulsar.client import PulsarClientWrapper
from tests.pulsar.enums import PulsarTopicName


class TestPubsubPlugin:
    def test_global_create_topics(self, pytester: Pytester, pulsar_client: PulsarClientWrapper) -> None:
        pytester.makeini(f"""
        [pytest]
        {Configuration.PULSAR_GLOBAL_TOPICS} = 
            {PulsarTopicName.GLOBAL_TOPIC_CREATE_ONE}
            {PulsarTopicName.GLOBAL_TOPIC_CREATE_TWO}
        """)
        pytester.copy_example("test_pulsar_plugin.py")
        result = pytester.runpytest("-k", "test_pulsar_global_create_topics")
        result.assert_outcomes(passed=1)

        topics = pulsar_client.client.get_topics(
            namespace=Defaults.PULSAR_NAMESPACE.value, tenant=Defaults.PULSAR_TENANT.value
        )
        assert any(PulsarTopicName.GLOBAL_TOPIC_CREATE_ONE in topic for topic in topics)
        assert any(PulsarTopicName.GLOBAL_TOPIC_CREATE_TWO in topic for topic in topics)

    def test_global_delete_topics(self, pytester: Pytester, pulsar_client: PulsarClientWrapper) -> None:
        pytester.makeini(f"""
        [pytest]
        {Configuration.PULSAR_GLOBAL_TOPICS} = 
            {PulsarTopicName.GLOBAL_TOPIC_DELETE_ONE}
            {PulsarTopicName.GLOBAL_TOPIC_DELETE_TWO}

        {Configuration.PULSAR_GLOBAL_DELETE} = True
        """)
        pytester.copy_example("test_pulsar_plugin.py")
        result = pytester.runpytest("-k", "test_pulsar_global_delete_topics")
        result.assert_outcomes(passed=1)

        topics = pulsar_client.client.get_topics(
            namespace=Defaults.PULSAR_NAMESPACE.value, tenant=Defaults.PULSAR_TENANT.value
        )
        assert all(PulsarTopicName.GLOBAL_TOPIC_DELETE_ONE not in topic for topic in topics)
        assert all(PulsarTopicName.GLOBAL_TOPIC_DELETE_TWO not in topic for topic in topics)
