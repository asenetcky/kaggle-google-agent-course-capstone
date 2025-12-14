.PHONY: install install-dev ruff run ui docker-build docker-run docker-stop

install:
	uv sync --no-dev

install-dev:
	uv sync

ruff:
	uvx ruff check --select I --fix
	uvx ruff format

run:
	uv run ./src/toddle_ops/main.py

ui:
	uv run streamlit run src/toddle_ops/ui.py

docker-build:
	docker build -t toddle-ops:latest .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f toddle-ops
