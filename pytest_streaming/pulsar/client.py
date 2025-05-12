from httpx import URL
from httpx import Client as HttpxClient
from httpx import Headers
from httpx import QueryParams
from httpx import Response
from pulsar import Client as PulsarClient  # type: ignore[import-untyped]


class PulsarClientWrapper(PulsarClient):  # type: ignore[misc]
    USER_AGENT: str = "Pytest-Streaming"
    CONTENT_TYPE: str = "application/json"
    CONNECTION_TIMEOUT_SECONDS: int = 5

    def __init__(self, service_url: str, admin_url: str) -> None:
        super().__init__(service_url=service_url)
        self.admin_url = admin_url
        self.client = HttpxClient(
            timeout=self.CONNECTION_TIMEOUT_SECONDS,
            headers=Headers(
                {
                    "User-Agent": self.USER_AGENT,
                    "Content-Type": self.CONTENT_TYPE,
                }
            ),
        )

    @property
    def admin_endpoint(self) -> str:
        url = self.admin_url.rstrip("/")
        return f"{url}/admin/v2"

    def setup_testing_topics(self, topics: list[str], tenant: str, namespace: str) -> None:
        for topic in topics:
            self._create_topic(topic_name=topic, tenant=tenant, namespace=namespace)

    def delete_testing_topics(self, topics: list[str], tenant: str, namespace: str) -> None:
        for topic in topics:
            self._delete_topic(topic_name=topic, tenant=tenant, namespace=namespace)

    def _get_topics(self, tenant: str, namespace: str) -> list[str]:
        url = URL(f"{self.admin_endpoint}/persistent/{tenant}/{namespace}")
        resp: Response = self.client.get(url)
        assert resp.status_code == 200, f"Failed to get topics: {resp.text}"
        res = resp.json()
        assert isinstance(res, list)
        return res

    def _get_namespaces(self, tenant: str) -> list[str]:
        url = URL(f"{self.admin_endpoint}/namespaces/{tenant}")
        resp: Response = self.client.get(url)
        assert resp.status_code == 200, f"Failed to get namespaces: {resp.text}"
        res = resp.json()
        assert isinstance(res, list)
        return res

    def _create_topic(self, topic_name: str, tenant: str, namespace: str) -> None:
        topic = f"persistent://{tenant}/{namespace}/{topic_name}"
        self.create_producer(topic)

    def _delete_topic(self, topic_name: str, tenant: str, namespace: str) -> None:
        url = URL(f"{self.admin_endpoint}/persistent/{tenant}/{namespace}/{topic_name}")
        resp = self.client.delete(url, params=QueryParams({"force": "true"}))
        assert resp.status_code == 204, f"Failed to delete topic: {resp.text}"

    # FIXME: integrate this functionality and add coverage
    def _delete_namespace(self, tenant: str, namespace: str) -> None:  # pragma: no cover
        topics = self._get_topics(tenant=tenant, namespace=namespace)
        for topic in topics:
            self._delete_topic(topic_name=topic.split("/")[-1], tenant=tenant, namespace=namespace)

        # never delete the default namespace
        if namespace == "default":
            return

        url = URL(f"{self.admin_endpoint}/namespaces/{tenant}/{namespace}")
        resp = self.client.delete(url)
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

        url = URL(f"{self.admin_endpoint}/tenants/{tenant}")
        resp = self.client.delete(url)
        assert resp.status_code in [204, 404], f"Failed to delete tenant: {resp.text}"
