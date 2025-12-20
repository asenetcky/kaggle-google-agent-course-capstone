.PHONY: install install-dev ruff run ui adk-web test test-research test-orchestrator

install:
	uv sync --no-dev

install-dev:
	uv sync

ruff:
	uvx ruff check --select I --fix
	uvx ruff format

run:
	uv run src/toddle_ops/main.py

ui:
	uv run streamlit run src/toddle_ops/ui.py

# TODO: consider forcing meory:// for --artifact_service_uri
# TODO: consider a version of adk web that connects to supabase with --session_service_uri
adk-web:
	uv run adk web src/toddle_ops/agents/ --artifact_service_uri="memory://"

test:
	uv run pytest tests/ -v

test-research:
	uv run adk eval src/toddle_ops/agents/research_team src/toddle_ops/agents/research_team/research_team.evalset.json --config_file_path=src/toddle_ops/agents/research_team/test_config.json --print_detailed_results

test-orchestrator:
	uv run adk eval src/toddle_ops/agents/orchestrator src/toddle_ops/agents/orchestrator/orchestrator.evalset.json --config_file_path=src/toddle_ops/agents/orchestrator/test_config.json --print_detailed_results
