from google.cloud import pubsub_v1  # type: ignore[import-untyped]
from google.api_core.exceptions import NotFound


class GCPPublisher(pubsub_v1.PublisherClient):  # type: ignore[misc]
    """A Google Cloud Pub/Sub Publisher client.

    This class extends the Google Cloud Pub/Sub Publisher client
    to provide additional functionality for managing topics.
    """

    def setup_testing_topics(self, project_id: str, topics: list[str]) -> None:
        """Creates Pub/Sub topics for testing.

        Args:
            project_id: GCP project
            topics: List of topic names to create
        """
        self.delete_testing_topics(project_id, topics)
        for topic in topics:
            topic_path = self.topic_path(project_id, topic)
            self.create_topic(name=topic_path)

    def delete_testing_topics(self, project_id: str, topics: list[str]) -> None:
        """Deletes Pub/Sub topics for testing.

        Args:
            project_id: GCP project ID
            topics: List of topic names to delete
        """
        for topic in topics:
            try:
                topic_path = self.topic_path(project_id, topic)
                self.delete_topic(topic_path)
            except NotFound:
                pass
