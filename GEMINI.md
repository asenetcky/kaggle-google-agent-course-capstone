# Gemini Project Documentation

This file will contain documentation related to the Gemini project.

## Initial Setup

*   **Project Name:** toggle-ops
*   **Python Version:** Python 3.13 (as per `pyproject.toml` and `.python-version`)
*   **Dependencies:**
    *   `google-adk>=1.19.0`
    *   `marimo>=0.18.0`

## Project Structure (Key Directories)

*   `src/toddle_ops/agents/craft_research_team/`: Contains the research team agent logic.
*   `src/toddle_ops/agents/materials_team/`: Contains the materials team agent logic.
*   `src/toddle_ops/agents/project_database_team/`: Contains the project database team agent logic.
*   `src/toddle_ops/agents/project_history_team/`: Contains the project history team agent logic.
*   `src/toddle_ops/agents/quality_assurance_team/`: Contains the quality assurance team agent logic.
*   `src/toddle_ops/agents/root_agent/`: Contains the root agent logic for overall orchestration.
*   `notebooks/`: Contains marimo notebooks for agent development and testing.
*   `docs/`: Quarto-generated documentation.


## QA Team Workflow

The `notebooks/qa-team-mvp.py` notebook implements a multi-agent workflow for ensuring the quality of craft projects. The workflow is as follows:

1.  **Research:** A `ParallelAgent` (`CraftResearchTeam`) researches silly and science-related crafts.
2.  **Safety Assurance:** An `LlmAgent` (`SafetyAssuranceAgent`) assesses the safety of the proposed projects.
3.  **Approval:** An `LlmAgent` (`ProjectApprover`) approves or rejects the project based on the safety report.
4.  **Routing:** An `LlmAgent` (`Router`) conditionally routes the project to the editorial team if approved.
5.  **Editing:** A `SequentialAgent` (`EditorialTeam`) checks the project for clarity and grammar.

## How to Run Tests

1.  **Install test dependencies:** `uv pip install -e .[test]`
2.  **Run tests:** `uv run pytest`

## To-Do

*   Add deployment instructions.

**Note:** The project structure for agent directories has been updated to reflect their actual location under `src/toddle_ops/agents/`.

---
*This document is a placeholder and will be expanded as the project develops.*