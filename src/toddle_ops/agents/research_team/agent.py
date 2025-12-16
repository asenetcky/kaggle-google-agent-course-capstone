from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

from toddle_ops.config import retry_config
from toddle_ops.models.agents import AgentInstructions
from toddle_ops.models.projects import StandardProject
from toddle_ops.agents.research_team.sub_agent import default_temp_project_researcher
from toddle_ops.agents.research_team.workflows import research_sequence
from google.adk.tools import AgentTool



# Define instructions for the Project Synthesizer Agent
research_coordinator_instructions = AgentInstructions(
    persona="Project Research Coordinator",
    primary_objective=[
        "Analyze research output from the Project Researcher and create a single, sensible toddler project."
    ],
    rules=[
        "You can either pick the best parts from the project from the provided research, or combine elements to create a new project.",
        "Your output MUST be a `StandardProject` object.",
    ],
    constraints=[],
    incoming_keys=["low_temp_project_research", "high_temp_project_research", "default_temp_project_research"],
)

# Create the Project Synthesizer Agent using the defined instructions


root_agent = LlmAgent(
    name="ProjectResearchCoordinator",
    description="Coordinates research team to create toddler projects.",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=research_coordinator_instructions.format_instructions(),
    output_schema=StandardProject,
    output_key="standard_project",
    tools=[
       AgentTool(research_sequence),
       AgentTool(default_temp_project_researcher), 
    ],
)