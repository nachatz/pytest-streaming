# Getting started quickly

For a quick start, you can follow these steps

### Install pytest-streaming

```shell
pip install pytest-streaming
```

&#160;

### Utilize the decorator for the streaming technology of your choice

Detailed specifications and usage can be found here

- [Pulsar](./pulsar.md)
- [Pubsub](./pubsub.md)

&#160;

### Base Pulsar example

#### Setting up a local environment - Pulsar

If you're using docker compose, adding this for pulsar will get you
up and running end to end (`docker-compose.yml`)

```yaml
services:
  pulsar:
    image: apachepulsar/pulsar:latest
    container_name: pulsar
    ports: ['6650:6650', '8080:8080']
    environment:
    - PULSAR_STANDALONE_ENABLED=true
    - allowAutoTopicCreation=true
    command: [bin/pulsar, standalone]
```

Now you can run: `docker compose up -d` to have pulsar locally bootstrapped.

&#160;

#### Using the pulsar marker

You can simply create test specific topics on any
unit or integration test by leveraging the associated
marker, for example

```python
class TestPulsarProducer:
    @pytest.mark.pulsar(topics=["test-topic1", "test-topic2"])
    def test_pubsub_marker_topic_creation_base(self) -> None:
        # these pulsar topics are now available and completely clean
        # note these live by default in `public/default` namespace
        ...
```

Everything will be created and cleaned up for you by default on every
test run. Each decorator has a suite of customizable features. Read the
[documentation](https://nachatz.github.io/pytest-streaming) to see other parameters you can use and how you can create
topics for global use (integration tests).

&#160;

### Adding to your CI/CD

Running this in CI/CD is as simple as ensuring pulsar (or other streaming choice)
is running in the network. For the example above, adding this step to your GitHub action
will yield all the setup required

```yaml
- name: run docker-compose
    run: |
    docker compose up -d
    sleep 5s
```

&#160;
