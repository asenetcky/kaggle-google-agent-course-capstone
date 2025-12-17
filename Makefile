.PHONY: install install-dev ruff run ui test-research

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

test-research:
	uv run adk eval src/toddle_ops/agents/research_team src/toddle_ops/agents/research_team/research_team.evalset.json --config_file_path=src/toddle_ops/agents/research_team/test_config.json --print_detailed_results
