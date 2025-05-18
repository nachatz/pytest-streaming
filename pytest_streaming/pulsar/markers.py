from contextlib import contextmanager
from enum import StrEnum
from functools import cached_property
from typing import Generator
from typing import cast

from pytest_streaming.abstracts.markers import BaseMarker
from pytest_streaming.config import Configuration
from pytest_streaming.config import Defaults
from pytest_streaming.pulsar._models import TopicMeta
from pytest_streaming.pulsar.client import PulsarClientWrapper


class PulsarMarkerParams(StrEnum):
    """Shared parameters across all pulsar markers."""

    TOPICS = "topics=list"
    DELETE_AFTER = "delete_after=bool"
    SERVICE_URL = "service_url=str"
    ADMIN_URL = "admin_url=str"

    # TODO: add support for tenant and namespace parameters
    # TENANT = "tenant=str"
    # NAMESPACE = "namespace=str"

    def root(self) -> str:
        return self.value.split("=")[0]


class PulsarMarker(BaseMarker):
    """Primary pulsar marker for working with Pulsar topics.

    This marker allows you to create and delete Pulsar topics for testing purposes.
    It ensures the specified tenant and namespace exist before creating topics.
    By default, topics are recreated if they already exist.

    Attributes:
        - marker_name (str): name of the marker
        - marker_description (str): description of the marker
        - topics (list[str]): A list of Pulsar topic names to create.
        - delete_after (bool): If True, the topics will be deleted after the test. (default: False)
        - service_url (str): The Pulsar service URL. (default: from pytest.ini or Defaults.PULSAR_SERVICE_URL)
        - admin_url (str): The pulsar admin URL (default: from pytest.ini or Defaults.PULSAR_ADMIN_URL)

    Required Parameters:
        - topics (list[str])

    Optional Parameters:
        - delete_after (bool)
        - service_url (str)
        - admin_url (str)

    Example:
        ```python
        @pytest.mark.pulsar(topics=["topic-a", "topic-b"])
        def test_pulsar_topics():
            # Your test code here
            pass
        ```
    """

    marker_name: str = "pulsar"
    marker_description: str = "Create specified Pulsar topics automatically for the test."
    marker_params: list[str] = [param.value for param in PulsarMarkerParams]

    # Default values for the marker parameters
    _tenant: str = Defaults.PULSAR_TENANT.value
    _namespace: str = Defaults.PULSAR_NAMESPACE.value

    @property
    def topics(self) -> list[str]:
        if not self.marker:
            raise ValueError("Marker (pulsar) is not set")  # pragma: no cover

        topics = self.marker.kwargs.get(PulsarMarkerParams.TOPICS.root())
        if not topics or not isinstance(topics, list) or not all(isinstance(topic, str) for topic in topics):
            raise ValueError("No topics specified or invalid specification (list[str]) for the pulsar marker")
        return cast(list[str], topics)

    @property
    def delete_after(self) -> bool:
        if not self.marker:
            raise ValueError("Marker (pulsar) is not set")  # pragma: no cover

        delete_after = self.marker.kwargs.get(PulsarMarkerParams.DELETE_AFTER.root(), Defaults.PULSAR_AUTO_DELETE.value)
        if not isinstance(delete_after, bool):
            raise ValueError("Invalid specification for delete_after (bool)")  # pragma: no cover
        return delete_after

    @property
    def service_url(self) -> str:
        if not self.marker:
            raise ValueError("Marker (pulsar) is not set")  # pragma: no cover

        override_url = self.marker.kwargs.get(PulsarMarkerParams.SERVICE_URL.root())
        service_url = override_url or self.config.getini(Configuration.PULSAR_SERVICE_URL)
        if not isinstance(service_url, str):
            raise ValueError("Invalid specification for service_url (str)")  # pragma: no cover
        return service_url

    @property
    def admin_url(self) -> str:
        if not self.marker:
            raise ValueError("Marker (pulsar) is not set")  # pragma: no cover

        override_url = self.marker.kwargs.get(PulsarMarkerParams.ADMIN_URL.root())
        admin_url = override_url or self.config.getini(Configuration.PULSAR_ADMIN_URL)
        if not isinstance(admin_url, str):
            raise ValueError("Invalid specification for admin_url (str)")  # pragma: no cover
        return admin_url

    @property
    def _topic_meta(self) -> list[TopicMeta]:
        return [TopicMeta(topic_name=topic, tenant=self._tenant, namespace=self._namespace) for topic in self.topics]

    @cached_property
    def _pulsar_client(self) -> PulsarClientWrapper:
        return PulsarClientWrapper(service_url=self.service_url, admin_url=self.admin_url)

    @contextmanager
    def impl(self) -> Generator[None, None, None]:
        if not self.marker:
            yield
            return

        try:
            self._pulsar_client.setup_testing_topics(topics=self._topic_meta)

            yield

            if self.delete_after:
                self._pulsar_client.delete_testing_topics(topics=self._topic_meta)
        finally:
            self._pulsar_client.close()
