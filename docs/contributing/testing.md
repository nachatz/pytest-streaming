# Testing

All code must maintain 100% test coverage. This ensures that every line of code is exercised by the test suite and helps prevent regressions.

## Validating Changes

To validate your changes, run:

```shell
just check
```

This command runs linting, formatting, and the full test suite. All checks must pass before submitting a pull request.

## Focus

Tests should be high quality and cover both unit-testable code and live integrations. This means you should:

- Write isolated unit tests for logic that can be tested independently.
- Ensure integration tests run against real Pub/Sub and Pulsar emulators to verify actual resource creation and cleanup.

Both types of tests are required to ensure correctness and reliability of the plugin in real-world scenarios.

## Continuous Integration

All checks, including linting, formatting, and the full test suite, are automatically run and validated by GitHub Actions when a pull request is opened. This ensures that every contribution meets the project's quality standards before it is merged.
