# Setting up for local development

This guide describes how to set up your environment for contributing to `pytest-streaming`.

## Prerequisites

1. Install [Docker](https://www.docker.com/) to run local emulators and dependencies.
2. Ensure you have [Just](https://github.com/casey/just) installed for running project tasks.
3. Make sure you have Python 3.11+ installed and available in your PATH.

## Running the setup script

Run the setup script to install Python dependencies and prepare your environment.

```shell
sh setup.sh
```

This will install the latest Python version and set up any additional tooling needed for development

1. Just
2. UV (python dependency management)
3. Python
4. Yamlfmt

## Running the starter just commands

The project uses a `justfile` to simplify common development tasks. To set up the project, run:

```shell
just setup
```

This will install dependencies and perform any other initial project configuration.

## Starting docker

To start the required Docker containers (such as Pub/Sub emulator and Pulsar), run:

```shell
just compose
```

This will launch all services defined in the `docker-compose.yml` file. Wait a few seconds for the containers to become healthy before running tests.

## Validating setup

To verify your environment is ready, run the following command to check formatting, linting, and run all tests:

```shell
just check
```

All tests, formatting, and linting should pass before you begin development or submit a pull request.
