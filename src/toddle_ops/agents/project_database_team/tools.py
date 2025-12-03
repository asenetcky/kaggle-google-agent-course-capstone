import json
import sqlite3
import uuid
from enum import Enum
from pathlib import Path
from typing import List, Optional

from toddle_ops.models.projects import Difficulty, Project

DATABASE_FILE = Path("toddle_ops_projects.db")


def _get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the database and creates the projects table if it doesn't exist."""
    conn = _get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            project_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            difficulty TEXT,
            duration_minutes INTEGER,
            materials TEXT,
            instructions TEXT
        )
    """)
    conn.commit()
    conn.close()


def create_project(project: Project) -> Project:
    """
    Creates a new project in the database.

    Args:
        project: The project object to create.

    Returns:
        The created project object.
    """
    conn = _get_db_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO projects (project_id, name, description, difficulty, duration_minutes, materials, instructions)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    materials_json = json.dumps([m.model_dump() for m in project.materials])
    instructions_json = json.dumps(project.instructions)

    cursor.execute(
        sql,
        (
            str(project.project_id),
            project.name,
            project.description,
            project.difficulty.value,
            project.duration_minutes,
            materials_json,
            instructions_json,
        ),
    )
    conn.commit()
    conn.close()
    return project


def get_project(project_id: str) -> Optional[Project]:
    """
    Retrieves a project from the database by its ID.

    Args:
        project_id: The ID of the project to retrieve.

    Returns:
        The project object if found, otherwise None.
    """
    conn = _get_db_connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM projects WHERE project_id = ?"
    cursor.execute(sql, (project_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return Project(
            project_id=uuid.UUID(row["project_id"]),
            name=row["name"],
            description=row["description"],
            difficulty=Difficulty(row["difficulty"]),
            duration_minutes=row["duration_minutes"],
            materials=json.loads(row["materials"]),
            instructions=json.loads(row["instructions"]),
        )
    return None


def update_project(project_id: str, updates: dict) -> Optional[Project]:
    """
    Updates a project in the database.

    Args:
        project_id: The ID of the project to update.
        updates: A dictionary of fields to update.

    Returns:
        The updated project object if the project was found and updated, otherwise None.
    """
    conn = _get_db_connection()
    cursor = conn.cursor()

    fields = []
    values = []
    for key, value in updates.items():
        if key in ["materials", "instructions"]:
            values.append(json.dumps(value))
        elif isinstance(value, Enum):
            values.append(value.value)
        else:
            values.append(value)
        fields.append(f"{key} = ?")

    if not fields:
        return get_project(project_id)

    sql = f"UPDATE projects SET {', '.join(fields)} WHERE project_id = ?"
    values.append(project_id)

    cursor.execute(sql, tuple(values))
    conn.commit()

    updated_rows = cursor.rowcount
    conn.close()

    if updated_rows > 0:
        return get_project(project_id)
    return None


def delete_project(project_id: str) -> bool:
    """
    Deletes a project from the database.

    Args:
        project_id: The ID of the project to delete.

    Returns:
        True if the project was deleted, otherwise False.
    """
    conn = _get_db_connection()
    cursor = conn.cursor()
    sql = "DELETE FROM projects WHERE project_id = ?"
    cursor.execute(sql, (project_id,))
    conn.commit()
    deleted_rows = cursor.rowcount
    conn.close()
    return deleted_rows > 0


def list_projects() -> List[Project]:
    """
    Lists all projects in the database.

    Returns:
        A list of all project objects.
    """
    conn = _get_db_connection()
    cursor = conn.cursor()
    sql = "SELECT * FROM projects"
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()

    return [
        Project(
            project_id=uuid.UUID(row["project_id"]),
            name=row["name"],
            description=row["description"],
            difficulty=Difficulty(row["difficulty"]),
            duration_minutes=row["duration_minutes"],
            materials=json.loads(row["materials"]),
            instructions=json.loads(row["instructions"]),
        )
        for row in rows
    ]


# add this in eventually
# tool_context: ToolContext
def ask_user_permission(summary: str) -> str:
    """
    Asks the user for permission to proceed with the summarized actions.

    Args:
        summary: A description of the proposed actions.

    Returns:
        'yes' if the user approves, 'no' otherwise.
    """
    print(f"\nPROPOSED DATABASE ACTIONS:\n{summary}\n")
    choice = input("Okay to proceed Y/n? ").strip().lower()
    if choice in ("y", "yes", ""):
        return "yes"
    return "no"
