from httpx import URL, Client as HttpxClient, Headers, QueryParams
from pulsar import Client as PulsarClient


class PulsarClientWrapper(PulsarClient):
    
    CONNECTION_TIMEOUT_SECONDS: int = 5
    USER_AGENT: str = "Pytest-Streaming"
    CONTENT_TYPE: str = "application/json"

    def __init__(self, service_url: str) -> None:
        super().__init__(service_url=service_url)
        self.client = HttpxClient(
            timeout=self.CONNECTION_TIMEOUT_SECONDS,
            headers=Headers(
                {
                    "User-Agent": self.USER_AGENT,
                    "Content-Type": self.CONTENT_TYPE,
                }
            ),
        )

    def setup_testing_topics(self, topics: list[str], tenant: str, namespace: str) -> None:
        for topic in topics:
            self.create_topic(topic_name=topic)

    def delete_testing_topics(self, admin_url: str, topics: list[str]) -> None:
        for topic in topics:
            self.delete_topic(admin_url=admin_url, topic_name=topic)

    def create_topic(self, topic_name: str) -> None:
        self.create_producer(topic_name)

    def delete_topic(self, admin_url: str, topic_name: str) -> None:
        url = URL(f"{admin_url}/admin/v2/persistent/public/default/{topic_name}")
        resp = self.client.delete(url, params=QueryParams({"force": "true"}))
        assert resp.status_code == 204, f"Failed to delete topic: {resp.text}"