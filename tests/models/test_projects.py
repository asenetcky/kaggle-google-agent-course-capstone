from __future__ import annotations

import uuid

from toddle_ops.models.projects import Difficulty, Project


def test_create_project():
    """Test creating a project with valid data."""
    project_data = {
        "name": "Test Project",
        "description": "A test project.",
        "difficulty": Difficulty.EASY,
        "duration_minutes": 30,
        "materials": [
            {"name": "paper", "quantity": 1, "units": "sheet"},
        ],
        "instructions": ["Step 1", "Step 2"],
    }
    project = Project(**project_data)
    assert project.name == project_data["name"]
    assert project.description == project_data["description"]
    assert project.difficulty == project_data["difficulty"]
    assert project.duration_minutes == project_data["duration_minutes"]
    assert len(project.materials) == 1
    assert project.materials[0].name == "paper"
    assert len(project.instructions) == 2
    assert isinstance(project.project_id, uuid.UUID)
