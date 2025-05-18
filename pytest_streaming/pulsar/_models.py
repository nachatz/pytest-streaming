class TopicMeta:
    def __init__(self, topic_name: str, tenant: str, namespace: str):
        self.topic_name = topic_name
        self.tenant = tenant
        self.namespace = namespace

    @property
    def path(self) -> str:
        return f"persistent/{self.tenant}/{self.namespace}/{self.topic_name}"

    @property
    def long(self) -> str:
        return f"persistent://{self.tenant}/{self.namespace}/{self.topic_name}"

    @property
    def short(self) -> str:
        return self.topic_name
