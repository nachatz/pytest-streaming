# Pulsar Global Usage

You can configure global topics to be created at the start of the test session and optionally deleted at the end. This is useful for integration tests that share topics across multiple tests.

## PyTest.ini Options

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