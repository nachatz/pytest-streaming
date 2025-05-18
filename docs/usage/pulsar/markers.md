# Pulsar Marker Usage

The `@pytest.mark.pulsar` marker allows you to create and optionally delete Pulsar topics for the duration of a test. This is useful for isolating test resources and ensuring a clean environment.

## Marker Parameters

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

## PyTest.ini Options (Marker Defaults)

You can set default values for marker parameters in your `pytest.ini` file. These will be used if the marker does not override them.

```
[pytest]
pytest_streaming_pulsar_service_url = pulsar://localhost:6650
pytest_streaming_pulsar_admin_url = http://localhost:8080
```