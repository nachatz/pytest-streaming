
install:
    mise install --yes

setup:
    uv sync

compose:
    docker compose down
    docker compose up -d

fmt:
    uv run ruff format
    uv run ruff check

mypy:
    uv run mypy --strict .

docs:
    uv run mkdocs serve