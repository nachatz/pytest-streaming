# PubSub Usage

This section describes how to use the Pub/Sub integration in `pytest-streaming` for managing topics in your tests. The plugin supports both global and per-test topic management using either `pytest.ini` configuration or test markers.

View the specification for verbose details on all usable interfaces of this [library](./../specification/pubsub.md)

&#160;

## PubSub Marker Usage

The `@pytest.mark.pubsub` marker allows you to create and optionally delete Pub/Sub topics for the duration of a test. This is useful for isolating test resources and ensuring a clean environment.

### Marker Parameters

The following parameters are supported by the `pubsub` marker:

- `topics` (list[str], required): List of Pub/Sub topic names to create for the test.
- `delete_after` (bool, optional): If `True`, topics are deleted after the test. Default is `False`. Resources are always cleaned up prior to each test run.
- `project_id` (str, optional): GCP project ID. Defaults to the value in `pytest.ini` or the plugin default of `pytest-streaming`.

**Examples:**

```python
import pytest

@pytest.mark.pubsub(topics=["test-topic-1", "test-topic-2"])
class TestPubsub:
    def test_topic_creation(self):
        # Test logic using the created topics
        pass
```

```python
import pytest

@pytest.mark.pubsub(topics=["test-topic-1", "test-topic-2"], delete_after=True)
class TestPubsub:
    def test_topic_creation(self):
        # Test logic using the created topics
        pass
```

```python
import pytest

@pytest.mark.pubsub(topics=["test-topic-1", "test-topic-2"], delete_after=True, project_id="my-gcp-project")
class TestPubsub:
    def test_topic_creation(self):
        # Test logic using the created topics
        pass
```

### PyTest.ini Options (Marker Defaults)

You can set default values for marker parameters in your `pytest.ini` file. These will be used if the marker does not override them.

```
[pytest]
pytest_streaming_pubsub_project_id = pytest-streaming
pytest_streaming_pubsub_emulator_enabled = true
```

`pytest_streaming_pubsub_emulator_enabled` is a optional parameter that defaults to True. It is a base safety to ensure you are targeting the pubsub emulator and not a live instance in Google Cloud. You can easily disable this by setting that value to `false`.

&#160;

## PubSub Global Usage

You can configure global topics to be created at the start of the test session and optionally deleted at the end. This is useful for integration tests that share topics across multiple tests.

### PyTest.ini Options

Add the following options to your `pytest.ini` to manage global topics. These must use the exact keys as defined by the plugin:

- `pytest_streaming_pubsub_global_topics` (linelist): New-line separated list of topics to create globally.
- `pytest_streaming_pubsub_global_delete` (bool): If `True`, global topics are deleted after the session. Default is `False`.
- `pytest_streaming_pubsub_project_id` (str): GCP project ID. Default is `pytest-streaming`.
- `pytest_streaming_pubsub_emulator_enabled` (bool): Ensures the Pub/Sub emulator is being used. Default is `true`.

**Example:**

```ini
[pytest]
pytest_streaming_pubsub_global_topics = 
    topic1 
    topic2

pytest_streaming_pubsub_global_delete = true
pytest_streaming_pubsub_project_id = pytest-streaming
pytest_streaming_pubsub_emulator_enabled = true
```

With these settings, the specified topics will be created at session start and deleted at session end if `pytest_streaming_pubsub_global_delete` is enabled.

**The project id will be the new default for all markers used within the test suite**, you can still override this as needed per test via the marker. The global delete will only affect the global topics stated above.

&#160;

## Setting up Pub/Sub

### Setting up Pub/Sub locally

If you have [Docker](https://www.docker.com/) installed, you can leverage a docker compose file to bootstrap the resources needed to run this locally and in CI/CD.

Create a file called `docker-compose.yml` and paste the following within it

```yaml
services:
  pubsub-emulator:
    image: google/cloud-sdk:latest
    command: gcloud beta emulators pubsub start --project=pytest-streaming --host-port=0.0.0.0:8432
    ports: ['8432:8432']
    environment:
      PUBSUB_PROJECT_ID: pytest-streaming
      PUBSUB_EMULATOR_HOST: localhost:8432
```

### Setting up Pub/Sub in CI/CD

The example provided is for GitHub actions, but if you are using other platforms (Jenkins, for example) the setup is mostly the same. Simply need to enable and start the **pubsub emulator** in your network.

Doing this with a GitHub action is as simple as leveraging the `docker-compose.yml` file setup in the previous step.

```yaml

name: test check
on:
  push:
    branches: [main]

  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout

    - name: run docker-compose
      run: |
        docker compose up -d
        sleep 10s

    - name: run test
      run: |-
        # your test command
```
