from contextlib import contextmanager
from enum import StrEnum
from typing import Generator
from pydantic import PrivateAttr

from pytest_streaming.abstracts.markers import AbstractMarker
from pytest_streaming.config import Configuration
from pytest_streaming.pubsub.publisher import GCPPublisher


class PubsubMarkerParams(StrEnum):
    """Shared parameters across all pubsub markers."""

    TOPICS = "topics=list"
    DELETE_AFTER = "delete_after=bool"
    PROJECT_ID = "project_id=str"


class PubsubMarker(AbstractMarker):

    marker_name: str = "pubsub"
    marker_description: str = "Create specified Pub/Sub topics automatically for the test."
    marker_params: list[str] = [
        PubsubMarkerParams.TOPICS,
        PubsubMarkerParams.DELETE_AFTER,
        PubsubMarkerParams.PROJECT_ID,
    ]

    _topics: None = PrivateAttr(default=None)
    _project_id: None = PrivateAttr(default=None)
    _delete_after: bool = PrivateAttr(default=False)

    @property
    def topics(self) -> list[str]:
        assert self.marker, "Marker is not set"
        topics = self.marker.kwargs.get(PubsubMarkerParams.TOPICS, self._topics)
        if not topics:
            raise ValueError("No topics specified for the pubsub marker")
        return topics
    
    @property
    def delete_after(self) -> bool:
        assert self.marker, "Marker is not set"
        return self.marker.kwargs.get(PubsubMarkerParams.DELETE_AFTER, self._delete_after)
    
    @property
    def project_id(self) -> str:
        assert self.marker, "Marker is not set"
        override_project_id = self.marker.kwargs.get(PubsubMarkerParams.PROJECT_ID, self._project_id)
        project_id = override_project_id or self.config.getini(Configuration.PUBSUB_PROJECT_ID)
        return project_id
        
    @contextmanager
    def impl(self) -> Generator[None, None, None]:
        """Creates and optionally deletes Pub/Sub topics for tests with the pubsub marker.

        Args:
            request: pytest fixture request object
            pytestconfig: pytest config object
        """
        if not self.marker:
            yield
            return

        GCPPublisher().setup_testing_topics(self.project_id, self.topics)

        yield

        if self.delete_after:
            GCPPublisher().delete_testing_topics(self.project_id, self.topics)