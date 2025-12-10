from sqlmodel import Field, Relationship, SQLModel


class StandardProject(SQLModel, table=True):
    """A craft project for toddlers."""

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, description="The name of the project.")
    description: str = Field(description="A brief description of the project.")
    duration_minutes: int = Field(
        description="The estimated duration of the project in minutes."
    )
    instructions: str = Field(
        description="Numbered, step by step instructions for the project."
    )

    materials: str = Field(description="Bulleted list of materials")


class Project(SQLModel, table=True):
    """A craft project for toddlers."""

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, description="The name of the project.")
    description: str = Field(description="A brief description of the project.")
    duration_minutes: int = Field(
        description="The estimated duration of the project in minutes."
    )
    instructions: str = Field(description="A list of instructions for the project.")

    materials: list["Material"] = Relationship(back_populates="project")


# materials_id: Optional[int] = Field(default=None, foreign_key="material.id")


class Material(SQLModel, table=True):
    """A material required for a project."""

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, description="The name of the material.")
    quantity: float = Field(description="The quantity of the material.")
    units: str | None = Field(default=None, description="The units of the material.")

    project_id: int | None = Field(default=None, foreign_key="project.id")
    project: Project | None = Relationship(back_populates="materials")
