default:
    @just --list

sync:
    uv sync --dev

test:
    uv run pytest

lint:
    uv run ruff check .
    uv run ruff format --check .

format:
    uv run ruff check --fix .
    uv run ruff format .

build:
    uv build

demo:
    rm -rf docs/_build
    uv run sphinx-build -W -b html docs docs/_build/html
