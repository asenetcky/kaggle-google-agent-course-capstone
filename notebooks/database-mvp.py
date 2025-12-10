# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "google-adk==1.20.0",
#     "litellm==1.80.8",
#     "protobuf==6.33.2",
#     "pydantic==2.12.5",
#     "python-dotenv==1.2.1",
#     "sqlmodel==0.0.27",
# ]
# ///

import marimo

__generated_with = "0.18.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from google.adk.agents import LlmAgent, ParallelAgent
    from google.adk.models.lite_llm import LiteLlm
    from google.adk.runners import InMemoryRunner

    return InMemoryRunner, LiteLlm, LlmAgent, ParallelAgent, mo


@app.cell
def _():
    from typing import List

    from pydantic import BaseModel
    from sqlmodel import Field, Relationship, SQLModel

    class ProjectBase(BaseModel):
        name: str = Field(index=True, description="The name of the project.")
        description: str = Field(description="A brief description of the project.")
        duration_minutes: int = Field(
            description="The estimated duration of the project in minutes."
        )
        instructions: str = Field(
            description="Step by step instructions for the project."
        )

    class Project(ProjectBase, SQLModel, table=True):
        """A craft project for toddlers."""

        id: int | None = Field(default=None, primary_key=True)
        materials: list["Material"] = Relationship(back_populates="project")

    # materials_id: Optional[int] = Field(default=None, foreign_key="material.id")

    class MaterialBase(BaseModel):
        name: str = Field(index=True, description="The name of the material.")
        quantity: float = Field(description="The quantity of the material.")
        units: str | None = Field(
            default=None, description="The units of the material."
        )

    class Material(MaterialBase, SQLModel, table=True):
        """A material required for a project."""

        id: int | None = Field(default=None, primary_key=True)
        project_id: int | None = Field(default=None, foreign_key="project.id")
        project: Project | None = Relationship(back_populates="materials")

    class ProjectPackage(BaseModel):
        project: ProjectBase
        materials: List[MaterialBase]

    return (ProjectPackage,)


@app.cell
def _(LiteLlm, LlmAgent, ProjectPackage):
    project_conversion_agent = LlmAgent(
        name="project_conversion_agent",
        # model=Gemini(model="gemini-2.5-flash-lite"),
        model=LiteLlm(model="ollama_chat/deepseek-r1:32b"),
        instruction="""You are adept at converting the
        provided to you into Project and Material Classes.""",
        output_schema=ProjectPackage,
    )
    return


@app.cell
def _():
    return


@app.cell
def _():
    # _runner = InMemoryRunner(agent=project_conversion_agent)
    # result = await _runner.run_debug(
    #     """
    #     You are given this this example project:

    #     Name: Toddler Art Project
    #     description: A simple art project for toddlers using basic materials.
    #     duration (in minutes): 30
    #     instructions: 1. Gather all materials. 2. Provide paper and crayons to the toddler.
    #         3. Encourage the toddler to draw freely. 4. Display the artwork proudly.
    #     materials:
    #        2 Sheets of paper, crayons (assorted colors), glue stick, safety scissors.

    #     Convert this information into the ProjectBase and MaterialBase classes, and
    #     return a ProjectPackage object containing the project and its materials.

    #     """
    # )
    return


@app.cell
def _():
    # result
    return


@app.cell
def _(mo):
    mo.md("""
    Okay I'm finding out that one big agent isn't working out too great. gemini-2.5-flash-lite works incredibly well - but I dont wanna pay if I can help it. Lets try parallel smaller agents
    """)
    return


@app.cell
def _(LiteLlm, LlmAgent):
    # smaller agents in parallel

    project_name_agent = LlmAgent(
        name="project_name_agent",
        model=LiteLlm(model="ollama_chat/gemma3:270m"),
        instruction="""Return ONLY the name of the project as text in your response and NOTHING ELSE.""",
        output_key="project_name",
    )

    project_description_agent = LlmAgent(
        name="project_description_agent",
        model=LiteLlm(model="ollama_chat/gemma3:4b"),
        instruction="""Return ONLY the description of the project in your response and NOTHING ELSE.""",
        output_key="project_description",
    )

    project_duration_agent = LlmAgent(
        name="project_duration_agent",
        model=LiteLlm(model="ollama_chat/gemma3:270m"),
        instruction="""Return ONLY the duration of the project in minutes as an integer and NOTHING ELSE.""",
        output_key="project_duration",
    )

    project_instructions_agent = LlmAgent(
        name="project_instructions_agent",
        model=LiteLlm(model="ollama_chat/gemma3:4b"),
        instruction="""Return ONLY the step by step instructions of the project as a single string and NOTHING ELSE.""",
        output_key="project_instructions",
    )

    project_materials_agent = LlmAgent(
        name="project_materials_agent",
        model=LiteLlm(model="ollama_chat/gemma3:1b"),
        instruction="""Return ONLY the materials required for the project as text in your response and NOTHING ELSE. """,
        output_key="project_materials",
    )
    return (
        project_description_agent,
        project_duration_agent,
        project_instructions_agent,
        project_materials_agent,
        project_name_agent,
    )


@app.cell
def _(
    ParallelAgent,
    project_description_agent,
    project_duration_agent,
    project_instructions_agent,
    project_materials_agent,
    project_name_agent,
):
    parallel_parser = ParallelAgent(
        name="parallel_project_parser",
        sub_agents=[
            project_name_agent,
            project_description_agent,
            project_duration_agent,
            project_instructions_agent,
            project_materials_agent,
        ],
    )
    return (parallel_parser,)


@app.cell
async def _(InMemoryRunner, parallel_parser):
    _runner = InMemoryRunner(agent=parallel_parser)
    await _runner.run_debug(
        """
        You are given this this example project:

        Name: Toddler Art Project
        description: A simple art project for toddlers using basic materials.
        duration (in minutes): 30
        instructions: 1. Gather all materials. 2. Provide paper and crayons to the toddler. 
            3. Encourage the toddler to draw freely. 4. Display the artwork proudly.
        materials:
           2 Sheets of paper, crayons (assorted colors), glue stick, safety scissors. 

        """
    )
    return


@app.cell
def _(mo):
    mo.md("""
    okay that works pretty well - let's refine materials
    """)
    return


@app.cell
async def _(InMemoryRunner, LiteLlm, LlmAgent):
    refined_material_agent = LlmAgent(
        name="refined_material_agent",
        model=LiteLlm(model="ollama_chat/gemma3:12b"),
        instruction="""Return ONLY the materials, their count and/or units required for the project as list of strings (list[str]) in your response and NOTHING ELSE. """,
        # output_schema=List[MaterialBase],
        output_key="refined_materials",
    )
    _runner = InMemoryRunner(agent=refined_material_agent)
    await _runner.run_debug(
        """
        You are given this this example project:

        Name: Toddler Art Project
        description: A simple art project for toddlers using basic materials.
        duration (in minutes): 30
        instructions: 1. Gather all materials. 2. Provide paper and crayons to the toddler. 
            3. Encourage the toddler to draw freely. 4. Display the artwork proudly.
        materials:
           2 Sheets of paper, crayons (assorted colors), glue stick, safety scissors. 

        """
    )
    return


@app.cell
async def _(InMemoryRunner, LiteLlm, LlmAgent):
    refined_instruction_agent = LlmAgent(
        name="refined_instruction_agent",
        model=LiteLlm(model="ollama_chat/gemma3:12b"),
        instruction="""Return ONLY the instructions required for the project as dictionary(dict[int, str]) where
        the key is the step number and the value is the instruction string in your response and NOTHING ELSE. """,
        output_key="refined_instructions",
    )
    _runner = InMemoryRunner(agent=refined_instruction_agent)
    await _runner.run_debug(
        """
        You are given this this example project:

        Name: Toddler Art Project
        description: A simple art project for toddlers using basic materials.
        duration (in minutes): 30
        instructions: 1. Gather all materials. 2. Provide paper and crayons to the toddler. 
            3. Encourage the toddler to draw freely. 4. Display the artwork proudly.
        materials:
           2 Sheets of paper, crayons (assorted colors), glue stick, safety scissors. 

        """
    )

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
