import uuid
from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class Difficulty(str, Enum):
    """The difficulty of the project."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Material(BaseModel):
    """A material required for a project."""

    name: str = Field(..., description="The name of the material.")
    quantity: float = Field(..., description="The quantity of the material.")
    units: str | None = Field(None, description="The units of the material.")


# Keeping it simple strings for now - crunch time for  deadline
# TODO ensue the components of Project are database friendly
class Project(BaseModel):
    """A craft project for toddlers."""

    # UUID is is causing issues with the db
    project_id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="A unique identifier for the project.",
    )
    name: str = Field(..., description="The name of the project.")
    description: str = Field(..., description="A brief description of the project.")
    duration_minutes: int = Field(
        ..., description="The estimated duration of the project in minutes."
    )
    materials: str = Field(  # List[Material] = Field(
        ..., description="A list of materials required for the project."
    )
    instructions: str = Field(  # List[str] = Field(
        ..., description="A list of instructions for the project."
    )


class SafetyStatus(str, Enum):
    """The safety status of a project."""

    APPROVED = "APPROVED"
    NEEDS_REVISION = "NEEDS_REVISION"


class SafetyReport(BaseModel):
    """A safety report for a project."""

    status: SafetyStatus = Field(..., description="The safety status of the project.")
    suggestions: List[str] = Field(
        default_factory=list,
        description="Suggestions for improving safety if revision is needed.",
    )
    summary: str = Field(..., description="A concise summary of the safety assessment.")
