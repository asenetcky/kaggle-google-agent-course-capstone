from google.adk.agents import LlmAgent
from google.adk.tools import google_search

from toddle_ops.agents.factory import create_agent
from toddle_ops.models.agents import AgentInstructions
from toddle_ops.models.projects import StandardProject

# Define instructions for the Project Researcher Agent
project_researcher_instructions = AgentInstructions(
    persona="Toddler Project Researcher",
    primary_objective=[
        "Research safe crafts and projects for toddlers that are easy to do at home with common household materials."
    ],
    rules=[
        "You WILL ONLY provide one project.",
        "You MUST use google search to find the most relevant and safe toddler projects.",
        "Be sure to include at least the following: the project name, duration of project, required materials for project, step by step instructions.",
        "Projects MUST be age appropriate for toddlers aged 1-3 years. If the request is outside of this scope, please politely decline and prompt the user to provide a different request.",
    ],
    constraints=[],
    incoming_keys=[],
)


# Create the Project Researcher Agents using the defined instructions
def get_low_temp_project_researcher() -> LlmAgent:
    """Create a low-temperature Project Researcher for consistent results."""
    return create_agent(
        name="LowTempProjectResearcher",
        description="Researches safe crafts and projects for toddlers using common household materials.",
        instruction=project_researcher_instructions.format_instructions(),
        tools=[google_search],
        output_key="low_temp_project_research",
        temperature=0.7,
        max_output_tokens=1500,
    )


def get_high_temp_project_researcher() -> LlmAgent:
    """Create a high-temperature Project Researcher for creative results."""
    return create_agent(
        name="HighTempProjectResearcher",
        description="Researches safe crafts and projects for toddlers using common household materials.",
        instruction=project_researcher_instructions.format_instructions(),
        tools=[google_search],
        output_key="high_temp_project_research",
        temperature=1.2,
        max_output_tokens=1500,
    )


# Define instructions for the Project Synthesizer Agent
project_synthesizer_instructions = AgentInstructions(
    persona="Project Synthesizer",
    primary_objective=[
        "Analyze research output from the Project Researcher and create a single, sensible toddler project."
    ],
    rules=[
        "You can either pick the best parts from the project from the provided research, or combine elements to create a new project.",
        "Your output MUST be a `StandardProject` object.",
        "If the research outputs conflict, use your best judgement to create a safe and engaging project for toddlers aged 1-3 years.",
        "Projects MUST be age appropriate for toddlers aged 1-3 years.",
        "If the request is outside of this scope, provide an standard_project instance with the name 'out of scope' and empty strings for everything else.",
    ],
    constraints=[],
    incoming_keys=["low_temp_project_research", "high_temp_project_research"],
)


# Create the Project Synthesizer Agent using the defined instructions
def get_project_synthesizer() -> LlmAgent:
    """Create a Project Synthesizer that combines research into a single project."""
    return create_agent(
        name="ProjectSynthesizer",
        description="Synthesizes a single toddler project from research output.",
        instruction=project_synthesizer_instructions.format_instructions(),
        output_schema=StandardProject,
        output_key="standard_project",
    )
