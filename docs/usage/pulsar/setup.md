# Setting up Pulsar

## Setting up Pulsar locally

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

## Setting up Pulsar in CI/CD

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
