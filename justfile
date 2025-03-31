
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

fmt-check:
    uv run ruff format --check
    uv run ruff check

mypy:
    uv run mypy --strict .

test:
    uv run pytest tests

docs:
    uv run mkdocs serve