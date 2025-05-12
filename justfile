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
    yamlfmt

fmt-check:
    uv run ruff format --check
    uv run ruff check
    yamlfmt -lint

mypy:
    uv run mypy --strict .

test:
    uv run coverage run -m pytest tests/ -vv
    uv run coverage report

check:
    just fmt
    just fmt-check
    just mypy
    just test

docs:
    uv run mkdocs serve