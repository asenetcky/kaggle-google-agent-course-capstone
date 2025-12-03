.PHONY: install install-dev ruff

install:
	uv sync --no-dev

install-dev:
	uv sync

ruff:
	uvx ruff check --select I --fix
	uvx ruff format
