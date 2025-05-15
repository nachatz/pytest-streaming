# Pulsar Usage

This section describes how to use the Pulsar integration in `pytest-streaming` for managing topics in your tests. The plugin supports both global and per-test topic management using either `pytest.ini` configuration or test markers.

&#160;

## Pulsar Marker Usage

The `@pytest.mark.pulsar` marker allows you to create and optionally delete Pulsar topics for the duration of a test. This is useful for isolating test resources and ensuring a clean environment.

### Marker Parameters

The following parameters are supported by the `pulsar` marker:

- `topics` (list[str], required): List of Pulsar topic names to create for the test.
- `delete_after` (bool, optional): If `True`, topics are deleted after the test. Default is `False`. Resources are always cleaned up prior to each test run.
- `service_url` (str, optional): Pulsar service URL. Defaults to the value in `pytest.ini` or the plugin default of `pulsar://localhost:6650`
- `admin_url` (str, optional): Pulsar admin URL. Defaults to the value in `pytest.ini` or the plugin default of `http://localhost:8080`

**Examples:**

```python
import pytest

@pytest.mark.pulsar(topics=["test-topic-1", "test-topic-2"])
class TestPulsar:
    def test_topic_creation(self):
        # Test logic using the created topics
        pass
```

```python
import pytest

@pytest.mark.pulsar(topics=["test-topic-1", "test-topic-2"], delete_after=True)
class TestPulsar:
    def test_topic_creation(self):
        # Test logic using the created topics
        pass
```

```python
import pytest

@pytest.mark.pulsar(topics=["test-topic-1", "test-topic-2"], delete_after=True, service_url="pulsar://localhost:1234")
class TestPulsar:
    def test_topic_creation(self):
        # Test logic using the created topics
        pass
```

### PyTest.ini Options (Marker Defaults)

You can set default values for marker parameters in your `pytest.ini` file. These will be used if the marker does not override them.

```
[pytest]
pytest_streaming_pulsar_service_url = pulsar://localhost:6650
pytest_streaming_pulsar_admin_url = http://localhost:8080
```

&#160;

## Pulsar Global Usage

You can configure global topics to be created at the start of the test session and optionally deleted at the end. This is useful for integration tests that share topics across multiple tests.

### PyTest.ini Options

Add the following options to your `pytest.ini` to manage global topics. These must use the exact keys as defined by the plugin:

- `pytest_streaming_pulsar_global_topics` (linelist): New-line separated list of topics to create globally.
- `pytest_streaming_pulsar_global_delete` (bool): If `True`, global topics are deleted after the session. Default is `False`.
- `pytest_streaming_pulsar_service_url` (str): Pulsar service URL default is `pulsar://localhost:6650`.
- `pytest_streaming_pulsar_admin_url` (str): Pulsar admin URL default is `http://localhost:8080`.

**Example:**

```ini
[pytest]
pytest_streaming_pulsar_global_topics = 
    topic1 
    topic2

pytest_streaming_pulsar_global_delete = true
pytest_streaming_pulsar_service_url = pulsar://localhost:6650
pytest_streaming_pulsar_admin_url = http://localhost:8080
```

With these settings, the specified topics will be created at session start and deleted at session end if `pytest_streaming_pulsar_global_delete` is enabled.

**The service url and admin url will be the new defaults for all markers used within the test suite**, you can still override these as needed per
test via the marker. The global delete will only affect the global topics stated above.

&#160;

## Setting up Pulsar

### Setting up Pulsar locally

If you have [Docker](https://www.docker.com/) installed,
you can leverage a docker compose file to bootstrap the
resources needed to run this locally and in CI/CD.

Create a file called `docker-compose.yml` and paste the
following within it

```yaml
services:
  pulsar:
    image: apachepulsar/pulsar:4.0.4
    container_name: pulsar
    ports: ['6650:6650', '8080:8080']
    environment:
    - PULSAR_STANDALONE_ENABLED=true
    - allowAutoTopicCreation=true
    command: [bin/pulsar, standalone]
```

### Setting up Pulsar in CI/CD

The example provided is for GitHub actions, but if you are using other platforms (Jenkins, for example)
the setup is mostly the same. Simply need to enable and start the **standalone** pulsar instance in your network.

Doing this with a GitHub action is as simple as leveraging the `docker-compose.yml` file setup in the previous
step.

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
