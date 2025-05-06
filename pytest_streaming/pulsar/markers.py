from contextlib import contextmanager
from enum import StrEnum
from typing import Generator
from typing import cast

from pytest_streaming.abstracts.markers import BaseMarker
from pytest_streaming.config import Configuration
from pytest_streaming.pulsar.client import PulsarClientWrapper


class PulsarMarkerParams(StrEnum):
    """Shared parameters across all pulsar markers."""

    TOPICS = "topics=list"
    DELETE_AFTER = "delete_after=bool"
    SERVICE_URL = "service_url=str"
    TENANT = "tenant=str"
    NAMESPACE = "namespace=str"

    def root(self) -> str:
        return self.value.split("=")[0]


class PulsarMarker(BaseMarker):
    """Primary pulsar marker for working with Pulsar topics.

    This marker allows you to create and delete Pulsar topics for testing purposes.
    It ensures the specified tenant and namespace exist before creating topics.
    By default, topics are recreated if they already exist.

    Required Parameters:
        - topics (list[str]): A list of Pulsar topic names to create.

    Optional Parameters:
        - delete_after (bool): If True, the topics will be deleted after the test. (default: False)
        - service_url (str): The Pulsar service URL. (default: from pytest.ini or Defaults.PULSAR_SERVICE_URL)
        - tenant (str): The Pulsar tenant. (default: from pytest.ini or Defaults.PULSAR_TENANT)
        - namespace (str): The Pulsar namespace. (default: from pytest.ini or Defaults.PULSAR_NAMESPACE)

    Example:
        ```python
        @pytest.mark.pulsar(topics=["topic-a", "topic-b"], delete_after=True, tenant="my-tenant")
        def test_pulsar_topics(request, pytestconfig):
            # Your test code here
            pass
        ```
    """

    marker_name: str = "pulsar"
    marker_description: str = "Create specified Pulsar topics automatically for the test."
    marker_params: list[str] = [
        PulsarMarkerParams.TOPICS,
        PulsarMarkerParams.DELETE_AFTER,
        PulsarMarkerParams.SERVICE_URL,
        PulsarMarkerParams.TENANT,
        PulsarMarkerParams.NAMESPACE,
    ]

    # Default values for the marker parameters
    _topics: None = None
    _service_url: None = None
    _delete_after: bool = False
    _tenant: str = "public"
    _namespace: str = "default"

    @property
    def topics(self) -> list[str]:
        if not self.marker:
            raise ValueError("Marker (pulsar) is not set")  # pragma: no cover

        topics = self.marker.kwargs.get(PulsarMarkerParams.TOPICS.root(), self._topics)
        if not topics or not isinstance(topics, list) or not all(isinstance(topic, str) for topic in topics):
            raise ValueError("No topics specified or invalid specification (list[str]) for the pulsar marker")
        return cast(list[str], topics)

    @property
    def delete_after(self) -> bool:
        if not self.marker:
            raise ValueError("Marker (pulsar) is not set")  # pragma: no cover
        return self.marker.kwargs.get(PulsarMarkerParams.DELETE_AFTER.root(), self._delete_after)

    @property
    def service_url(self) -> str:
        if not self.marker:
            raise ValueError("Marker (pulsar) is not set")  # pragma: no cover
        
        override_url = self.marker.kwargs.get(PulsarMarkerParams.SERVICE_URL.root(), self._service_url)
        service_url = override_url or self.config.getini(Configuration.PULSAR_SERVICE_URL)
        
        if not isinstance(service_url, str):
            raise ValueError("Invalid specification for service_url (str)")  # pragma: no cover
        return service_url

    @property
    def tenant(self) -> str:
        if not self.marker:
            raise ValueError("Marker (pulsar) is not set")  # pragma: no cover
        
        override_tenant = self.marker.kwargs.get(PulsarMarkerParams.TENANT.root(), self._tenant)
        tenant = override_tenant or self.config.getini(Configuration.PULSAR_TENANT)

        if not isinstance(tenant, str):
            raise ValueError("Invalid specification for tenant (str)")  # pragma: no cover
        return tenant

    @property
    def namespace(self) -> str:
        if not self.marker:
            raise ValueError("Marker (pulsar) is not set")  # pragma: no cover
        
        override_namespace = self.marker.kwargs.get(PulsarMarkerParams.NAMESPACE.root(), self._namespace)
        namespace = override_namespace or self.config.getini(Configuration.PULSAR_NAMESPACE)
        
        if not isinstance(namespace, str):
            raise ValueError("Invalid specification for namespace (str)")  # pragma: no cover
        return namespace

    @contextmanager
    def impl(self) -> Generator[None, None, None]:
        """Creates and optionally deletes Pulsar topics for tests with the pulsar marker."""
        if not self.marker:
            yield
            return

        client = PulsarClientWrapper(service_url=self.service_url)
        try:
            client.setup_testing_topics(
                tenant=self.tenant,
                namespace=self.namespace,
                topics=self.topics,
            )
            yield
        finally:
            if self.delete_after:
                client.delete_testing_topics(
                    tenant=self.tenant,
                    namespace=self.namespace,
                    topics=self.topics,
                )
            client.close()  # Ensure admin client connection is closed
