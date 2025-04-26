from contextlib import contextmanager
from enum import StrEnum
from typing import Generator
from typing import cast

from pytest_streaming.abstracts.markers import BaseMarker
from pytest_streaming.config import Configuration
from pytest_streaming.pubsub.publisher import GCPPublisher


class PubsubMarkerParams(StrEnum):
    """Shared parameters across all pubsub markers."""

    TOPICS = "topics=list"
    DELETE_AFTER = "delete_after=bool"
    PROJECT_ID = "project_id=str"

    def root(self) -> str:
        return self.value.split("=")[0]


class PubsubMarker(BaseMarker):
    """Primary pubsub marker for working with Pub/Sub topics.

    This marker allows you to create and delete Pub/Sub topics for testing purposes.
    It is used to set up the environment for tests that require Pub/Sub topics.
    By default, the topics are CREATE_OR_REPLACED, meaning that if they already exist, they will be replaced.

    Required Parameters:
        - topics (list[str]): A list of Pub/Sub topic names to create. (default: None)

    Optional Parameters:
        - delete_after (bool): If True, the topics will be deleted after the test. (default: False)
        - project_id (str): The GCP project ID where the topics will be created. (default: None)

    Example:
        ```python
        @pytest.mark.pubsub(topics=["topic1", "topic2"], delete_after=True, project_id="my-project-id")
        def test_pubsub_topics(request, pytestconfig):
            # Your test code here
            pass
        ```
    """

    marker_name: str = "pubsub"
    marker_description: str = "Create specified Pub/Sub topics automatically for the test."
    marker_params: list[str] = [
        PubsubMarkerParams.TOPICS,
        PubsubMarkerParams.DELETE_AFTER,
        PubsubMarkerParams.PROJECT_ID,
    ]

    # Default values for the marker parameters
    _topics: None = None
    _project_id: None = None
    _delete_after: bool = False

    @property
    def topics(self) -> list[str]:
        if not self.marker:
            raise ValueError("Marker (pubsub) is not set")

        topics = self.marker.kwargs.get(PubsubMarkerParams.TOPICS.root(), self._topics)
        if not topics or not isinstance(topics, list) or not all(isinstance(topic, str) for topic in topics):
            raise ValueError("No topics specified or invalid specification (list[str]) for the pubsub marker")
        return cast(list[str], topics)

    @property
    def delete_after(self) -> bool:
        if not self.marker:
            raise ValueError("Marker (pubsub) is not set")

        return self.marker.kwargs.get(PubsubMarkerParams.DELETE_AFTER.root(), self._delete_after)

    @property
    def project_id(self) -> str:
        if not self.marker:
            raise ValueError("Marker (pubsub) is not set")

        override_project_id = self.marker.kwargs.get(PubsubMarkerParams.PROJECT_ID.root(), self._project_id)
        project_id = override_project_id or self.config.getini(Configuration.PUBSUB_PROJECT_ID)
        if not isinstance(project_id, str):
            raise ValueError("Invalid specification for project_id (str)")

        return project_id

    @contextmanager
    def impl(self) -> Generator[None, None, None]:
        """Creates and optionally deletes Pub/Sub topics for tests with the pubsub marker."""
        if not self.marker:
            yield
            return

        safety = self.config.getini(Configuration.PUBSUB_EMULATOR_ENABLED)
        GCPPublisher().setup_testing_topics(self.project_id, self.topics, safety=safety)

        yield

        if self.delete_after:
            GCPPublisher().delete_testing_topics(self.project_id, self.topics, safety=safety)
