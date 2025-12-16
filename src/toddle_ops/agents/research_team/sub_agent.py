from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.genai import types

from toddle_ops.config import retry_config
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
        "Use google search to find the most relevant and safe toddler projects.",
        "Be sure to include at least the following: the project name, duration of project, required materials for project, step by step instructions.",
    ],
    constraints=[],
    incoming_keys=[],
)

# Create the Project Researcher Agents using the defined instructions
low_temp_project_researcher = LlmAgent(
    name="LowTempProjectResearcher",
    description="Researches safe crafts and projects for toddlers using common household materials.",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=project_researcher_instructions.format_instructions(),
    tools=[google_search],
    output_key="low_temp_project_research",
    generate_content_config=types.GenerateContentConfig(
        max_output_tokens=1000,
        temperature=0.7,
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            )
        ],
    ),
)

default_temp_project_researcher = LlmAgent(
    name="DefaultTempProjectResearcher",
    description="Researches safe crafts and projects for toddlers using common household materials.",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=project_researcher_instructions.format_instructions(),
    tools=[google_search],
    output_key="default_temp_project_research",
    generate_content_config=types.GenerateContentConfig(
        max_output_tokens=1000,
        temperature=1.0,
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            )
        ],
    ),
)

high_temp_project_researcher = LlmAgent(
    name="HighTempProjectResearcher",
    description="Researches safe crafts and projects for toddlers using common household materials.",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=project_researcher_instructions.format_instructions(),
    tools=[google_search],
    output_key="high_temp_project_research",
    generate_content_config=types.GenerateContentConfig(
        max_output_tokens=1000,
        temperature=1.2,
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            )
        ],
    ),
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
    ],
    constraints=[],
    incoming_keys=["low_temp_project_research", "high_temp_project_research", "default_temp_project_research"],
)

# Create the Project Synthesizer Agent using the defined instructions
project_synthesizer = LlmAgent(
    name="ProjectSynthesizer",
    description="Synthesizes a single toddler project from research output.",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=project_synthesizer_instructions.format_instructions(),
    output_schema=StandardProject,
    output_key="standard_project",
)
