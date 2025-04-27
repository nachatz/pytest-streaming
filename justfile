install:
    mise install --yes

setup:
    uv sync

compose:
    docker compose down
    docker compose up -d

fmt:
    uv run ruff check --select I --fix
    uv run ruff format
    uv run ruff format --check
    uv run ruff check

mypy:
    uv run mypy --strict .

test:
    uv run coverage run -m pytest tests/ -vv
    uv run coverage report

yml:
    uv run yamlfix .
    uv run yamllint .

check:
    just fmt
    just mypy
    just yml
    just test

docs:
    uv run mkdocs serve