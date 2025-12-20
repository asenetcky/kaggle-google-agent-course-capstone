from google.adk.agents import LlmAgent
from google.genai import types

from toddle_ops.agents.factory import DEFAULT_SAFETY_SETTINGS, create_agent
from toddle_ops.agents.research_team.workflows import get_research_sequence
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

def get_research_coordinator_agent() -> LlmAgent:
    """Create the Project Research Coordinator agent."""
    return create_agent(
        name="ProjectResearchCoordinator",
        description="Coordinates research team to create toddler projects.",
        instruction=research_coordinator_instructions.format_instructions(),
        output_key="standard_project",
        sub_agents=[get_research_sequence()],
        generate_content_config=types.GenerateContentConfig(
            max_output_tokens=1000,
            temperature=1.0,
            safety_settings=DEFAULT_SAFETY_SETTINGS,
        ),
    )


# Convenience alias for backwards compatibility
root_agent = get_research_coordinator_agent()
