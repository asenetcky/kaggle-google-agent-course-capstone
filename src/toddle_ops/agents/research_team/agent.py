from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types

from toddle_ops.agents.research_team.workflows import get_research_sequence
from toddle_ops.config import retry_config
from toddle_ops.models.agents import AgentInstructions

# Define instructions for the Project Synthesizer Agent
research_coordinator_instructions = AgentInstructions(
    persona="Project Research Coordinator",
    primary_objective=[
        "Coordinate the research team to create a safe and engaging toddler project suitable for children aged 1-3 years."
    ],
    rules=[
        "You MUST delegate tasks to your tools and sub-agents.",
        "Use the research_sequence to gather diverse project ideas.",
    ],
    constraints=[],
    incoming_keys=[],
)

# Create the Project Research Coordinator Agent using the defined instructions
root_agent = LlmAgent(
    name="ProjectResearchCoordinator",
    description="Coordinates research team to create toddler projects.",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=research_coordinator_instructions.format_instructions(),
    output_key="standard_project",
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
    sub_agents=[get_research_sequence()],
)
