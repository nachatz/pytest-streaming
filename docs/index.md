# PyTest Streaming

pytest-streaming is a PyTest plugin designed to simplify and automate the setup and teardown of streaming infrastructure for tests. It provides seamless integration for Google Pub/Sub, Apache Pulsar, Apache Kafka [WIP], and Nats [WIP] allowing you to create topics and subscriptions on demand, either globally or per test, using configuration or markers.

&#160;

## Concept

pytest-streaming enables efficient and reproducible testing of streaming applications by managing the lifecycle of topics and subscriptions. It supports both global and per-test resource management, making it suitable for local development and CI/CD pipelines. The plugin leverages PyTest's configuration system and marker mechanism to provide flexible control over streaming resources.

Key features:

- Automatic creation and cleanup of topics and subscriptions for streaming technologies
- Global configuration via `pytest.ini` or per-test control via markers
- Support for local emulators and containerized environments
- Class-based, type-hinted, and fixture-driven test patterns

The general flow for all created resources includes bootstrapping a net-new (clean) topic for the test.
By default, topics persist after the test for any validation/metrics collection needed. This however can be configured to auto delete after each run. By default, all topics are deleted and re-created on start of the test.

It's generally recommended to bootstrap global topics for integration tests (to avoid mocking out every dependent test) and utilize scoped topics for unit tests.

&#160;

## Supported

1. [Apache Pulsar](https://pulsar.apache.org/)
2. [Google PubSub](https://cloud.google.com/pubsub)
3. [[Coming soon] Kafka](https://kafka.apache.org/)
4. [[Coming soon] Nats](https://nats.io/)
5. [[Coming soon] Kinesis](https://aws.amazon.com/kinesis/)

&#160;

## Feedback and requests

Feedback, feature requests, and bug reports are welcome. Please open an issue or discussion on the [GitHub repository](https://github.com/nachatz/pytest-streaming).

&#160;

## Contributing

Contributions are encouraged. See the [contributing guide](contributing/contributing.md) for details on development, setup, and testing.
