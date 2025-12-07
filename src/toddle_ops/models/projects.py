import uuid
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, Relationship

from sqlmodel import SQLModel


class Difficulty(str, Enum):
    """The difficulty of the project."""

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Material(SQLModel, table=True):
    """A material required for a project."""

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, description="The name of the material.")
    quantity: float = Field(description="The quantity of the material.")
    units: str | None = Field(default=None, description="The units of the material.")

    projects: List["Project"] = Relationship(back_populates="materials")


class Project(SQLModel, table=True):
    """A craft project for toddlers."""

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, description="The name of the project.")
    description: str = Field(description="A brief description of the project.")
    duration_minutes: int = Field(
        description="The estimated duration of the project in minutes."
    )
    instructions: str = Field(description="A list of instructions for the project.")

    materials: list["Material"] = Relationship(back_populates="projects")
    materials_id: Optional[int] = Field(default=None, foreign_key="material.id")


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
