import os

from google.api_core.exceptions import NotFound
from google.cloud import pubsub_v1  # type: ignore[import-untyped]


class GCPPublisher(pubsub_v1.PublisherClient):  # type: ignore[misc]
    """A Google Cloud Pub/Sub Publisher client.

    This class extends the Google Cloud Pub/Sub Publisher client
    to provide additional functionality for managing topics.
    """

    @property
    def emulator_enabled(self) -> bool:
        return bool(os.getenv("PUBSUB_EMULATOR_HOST"))

    def setup_testing_topics(self, project_id: str, topics: list[str], safety: bool = True) -> None:
        """Creates Pub/Sub topics for testing.

        Args:
            project_id: GCP project
            topics: List of topic names to create
        """
        if safety and not self.emulator_enabled:
            raise EnvironmentError("Pubsub required to have the emulator enabled")

        project_path = f"projects/{project_id}"

        self.delete_testing_topics(project_id, topics)
        for topic in topics:
            topic_path = self.topic_path(project_id, topic)

            if topic_path in [t.name for t in self.list_topics(request={"project": project_path})]:  # pragma: no cover
                raise ValueError("Topic still exists and was not properly cleaned up prior to test run")
            self.create_topic(name=topic_path)

    def delete_testing_topics(self, project_id: str, topics: list[str], safety: bool = True) -> None:
        """Deletes Pub/Sub topics for testing.

        Args:
            project_id: GCP project ID
            topics: List of topic names to delete
        """
        if safety and not self.emulator_enabled:
            raise EnvironmentError("Pubsub required to have the emulator enabled")

        for topic in topics:
            try:
                topic_path = self.topic_path(project_id, topic)
                self.delete_topic(topic=topic_path)
            except NotFound:
                pass
