from httpx import URL
from httpx import Client as HttpxClient
from httpx import Headers
from httpx import QueryParams
from httpx import Response
from pulsar import Client as PulsarClient  # type: ignore[import-untyped]

from pytest_streaming.pulsar._models import TopicMeta


class AdminClient(HttpxClient):
    USER_AGENT: str = "pytest-streaming"
    CONTENT_TYPE: str = "application/json"
    CONNECTION_TIMEOUT_SECONDS: int = 5

    def __init__(self, base_url: str) -> None:
        url = URL(f"{base_url.rstrip('/')}/admin/v2")
        super().__init__(
            base_url=url,
            timeout=self.CONNECTION_TIMEOUT_SECONDS,
            headers=Headers(
                {
                    "User-Agent": self.USER_AGENT,
                    "Content-Type": self.CONTENT_TYPE,
                }
            ),
        )

    def get_topics(self, tenant: str, namespace: str) -> list[str]:
        url = URL(f"persistent/{tenant}/{namespace}")
        resp: Response = self.get(url)
        resp.raise_for_status()
        res = resp.json()
        assert isinstance(res, list)
        return res

    def delete_topic(self, topic: TopicMeta) -> None:
        url = URL(topic.path)
        resp = self.delete(url, params=QueryParams({"force": "true"}))
        assert resp.status_code in [204, 404], f"Failed to delete topic: {resp.text}"

    # FIXME: integrate this functionality and add coverage
    def _get_namespaces(self, tenant: str) -> list[str]:  # pragma: no cover
        url = URL(f"/namespaces/{tenant}")
        resp: Response = self.get(url)
        resp.raise_for_status()
        res = resp.json()
        assert isinstance(res, list)
        return res

    # FIXME: integrate this functionality and add coverage
    def _delete_namespace(self, tenant: str, namespace: str) -> None:  # pragma: no cover
        topics = self.get_topics(tenant=tenant, namespace=namespace)
        for topic in topics:
            topic_meta = TopicMeta(topic_name=topic.split("/")[-1], tenant=tenant, namespace=namespace)
            self.delete_topic(topic=topic_meta)

        # never delete the default namespace
        if namespace == "default":
            return

        url = URL(f"/namespaces/{tenant}/{namespace}")
        resp = self.delete(url)
        assert resp.status_code in [204, 404], f"Failed to delete namespace: {resp.text}"

    # FIXME: integrate this functionality and add coverage
    def _delete_tenant(self, tenant: str) -> None:  # pragma: no cover
        namespaces = self._get_namespaces(tenant=tenant)
        for namespace_path in namespaces:
            # never delete the functions namespace
            if namespace_path == "public/functions":
                continue
            namespace = namespace_path.split("/")[-1]
            self._delete_namespace(tenant=tenant, namespace=namespace)

        # never delete the default tenant
        if tenant == "public":
            return

        url = URL(f"/tenants/{tenant}")
        resp = self.delete(url)
        assert resp.status_code in [204, 404], f"Failed to delete tenant: {resp.text}"


class PulsarClientWrapper(PulsarClient):  # type: ignore[misc]
    def __init__(self, service_url: str, admin_url: str) -> None:
        super().__init__(service_url=service_url)
        self.admin_url = admin_url
        self.client = AdminClient(base_url=self.admin_url)

    def setup_testing_topics(self, topics: list[TopicMeta]) -> None:
        for topic in topics:
            self.client.delete_topic(topic=topic)
            found_topics = self.client.get_topics(tenant=topic.tenant, namespace=topic.namespace)

            if any(topic.short in t for t in found_topics):  # pragma: no cover
                raise ValueError("Topic still exists and was not properly cleaned up prior to test run")
            self._create_topic(topic=topic)

    def delete_testing_topics(self, topics: list[TopicMeta]) -> None:
        for topic in topics:
            self.client.delete_topic(topic=topic)

    def _create_topic(self, topic: TopicMeta) -> None:
        self.create_producer(topic.long)
