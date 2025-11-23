# Gemini Project Documentation

This file will contain documentation related to the Gemini project.

## Initial Setup

*   **Project Name:** kaggle-google-agent-course-capstone
*   **Python Version:** Python 3.13 (as per `pyproject.toml` and `.python-version`)
*   **Dependencies:**
    *   `google-adk>=1.19.0`
    *   `marimo>=0.18.0`

## Project Structure (Key Directories)

*   `src/craft_research_team/`: Contains the research team agent logic.
*   `src/quality_assurance_team/`: Contains the quality assurance team agent logic.
*   `notebooks/`: Contains marimo notebooks for agent development and testing.
*   `docs/`: Quarto-generated documentation.

## How to Run/Develop (Inferred)

1.  **Install dependencies:** `uv pip install -e .`
2.  **Run the QA Team notebook:** `uvx marimo edit --sandbox notebooks/qa-team-mvp.py`

## QA Team Workflow

The `notebooks/qa-team-mvp.py` notebook implements a multi-agent workflow for ensuring the quality of craft projects. The workflow is as follows:

1.  **Research:** A `ParallelAgent` (`CraftResearchTeam`) researches silly and science-related crafts.
2.  **Safety Assurance:** An `LlmAgent` (`SafetyAssuranceAgent`) assesses the safety of the proposed projects.
3.  **Approval:** An `LlmAgent` (`ProjectApprover`) approves or rejects the project based on the safety report.
4.  **Routing:** An `LlmAgent` (`Router`) conditionally routes the project to the editorial team if approved.
5.  **Editing:** A `SequentialAgent` (`EditorialTeam`) checks the project for clarity and grammar.

## To-Do

*   Document the purpose and usage of `src/craft_research_team/` and `src/quality_assurance_team/`.
*   Explain how to run tests (if any are added).
*   Add deployment instructions.

---
*This document is a placeholder and will be expanded as the project develops.*