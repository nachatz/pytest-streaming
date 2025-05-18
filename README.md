<h1 align="center">
Pytest Streaming
</h1>

<p align="center">
<img src="https://raw.githubusercontent.com/nachatz/pytest-streaming/main/docs/assets/icon.png" width="256" height="256">
</p>

<h3 align="center">
Augmenting and simplifying the flow of testing streaming applications including pulsar, google pubsub, kafka, and nats.
</h3>

<div align="center">

[![semantic-release: python](https://img.shields.io/badge/semantic--release-python-43e143?logo=semantic-release)](https://github.com/semantic-release/semantic-release)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pytest-streaming)
[![Tests](https://github.com/nachatz/pytest-streaming/actions/workflows/test.yml/badge.svg?branch=main)](https://github.com/nachatz/pytest-streaming/actions/workflows/test.yml)
[![Formatting](https://github.com/nachatz/pytest-streaming/actions/workflows/fmt.yml/badge.svg?branch=main)](https://github.com/nachatz/pytest-streaming/actions/workflows/fmt.yml)
[![Typing](https://github.com/nachatz/pytest-streaming/actions/workflows/mypy.yml/badge.svg?branch=main)](https://github.com/nachatz/pytest-streaming/actions/workflows/mypy.yml)
[![Docs](https://github.com/nachatz/pytest-streaming/actions/workflows/deploy_docs.yml/badge.svg?branch=main)](https://github.com/nachatz/pytest-streaming/actions/workflows/deploy_docs.yml)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

</div>

<div align="center">

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)
![Apache](https://img.shields.io/badge/apache-%23D42029.svg?style=for-the-badge&logo=apache&logoColor=white)
![Google Cloud](https://img.shields.io/badge/GoogleCloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white)

</div>

## Documentation

PyTest streaming documentation can be found [here](https://nachatz.github.io/pytest-streaming).

## Description

This PyTest plugin makes it easy to test streaming functionality (unit, integration, test, etc) through
seamless and easy to use decorators. The plugin currently supports bootstrapping of resources for the following
technologies

1. [Apache Pulsar](https://pulsar.apache.org/)
2. [Google PubSub](https://cloud.google.com/pubsub)
3. [[Coming soon] Kafka](https://kafka.apache.org/)
4. [[Coming soon] Nats](https://nats.io/)
5. [[Coming soon] Kinesis](https://aws.amazon.com/kinesis/)

The only setup the user needs to take is to have these running locally (ideally via Docker). Docker compose
files are provided for each of these, with formal documentation on how to setup everything easily in
CI/CD as well.

&#160;

## Quick start

To get started, you should reference the extensive documentation page found [here](https://nachatz.github.io/pytest-streaming).

For a quick start, you can follow these steps

### Install pytest-streaming

```shell
pip install pytest-streaming
```

&#160;

### Utilize the decorator for the streaming technology of your choice

If you're using docker compose, adding this for pulsar will get you
up and running end to end (`docker-compose.yml`)

```yml
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

Lastly, you can simply create test specific topics

```python
class TestPulsarProducer:
    @pytest.mark.pulsar(topics=["test-topic1", "test-topic2"])
    def test_pubsub_marker_topic_creation_base(self) -> None:
        # these pulsar topics are now available and completely clean
        ...
```

Everything will be created and cleaned up for you by default on every
test run. Each decorator has a suite of customizable features. Read the
[documentation](https://nachatz.github.io/pytest-streaming) to see other parameters you can use and how you can create
topics for global use (integration tests).

&#160;

### Adding to your CI/CD

Running this in CI/CD is as simple and ensuring pulsar (or other streaming choice)
is running in the network. For the example above, adding this step to your GitHub action
will yield all the setup required

```yml
- name: run docker-compose
    run: |
    docker compose up -d
    sleep 5s
```

&#160;

## Examples

A suite of examples which are provided and ran within the test suite directly
to verify functionality. These can be found under the [`examples`](./examples/) directory
at the root level of this project.
