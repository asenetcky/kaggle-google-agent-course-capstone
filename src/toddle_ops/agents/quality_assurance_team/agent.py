from google.adk.agents import LlmAgent
from google.genai import types
from toddle_ops.agents.factory import DEFAULT_SAFETY_SETTINGS, create_agent
from toddle_ops.models.agents import AgentInstructions
from toddle_ops.models.reports import StatusReport
from toddle_ops.agents.quality_assurance_team.workflows import quality_assurance_sequence


qa_coordinator_instructions = AgentInstructions(
    persona="Quality Assurance Team Lead",
    primary_objective=[
        "Oversee the quality assurance process to ensure toddler projects are safe, engaging, and appropriate for children aged 1-3 years."
    ],
    rules=[
        "Delegate tasks to the quality_assurance_sequence for thorough review and refinement.",
        "Ensure that all feedback is incorporated effectively to enhance the project quality.",
    ],
    constraints=[],
    incoming_keys=["standard_project"],
)
def get_quality_assurance_coordinator_agent() -> LlmAgent:
    """Create the Quality Assurance Team Lead agent."""
    return create_agent(
        name="QualityAssuranceCoordinator",
        description="Leads the quality assurance team to ensure toddler projects meet safety and quality standards.",
        instruction=qa_coordinator_instructions.format_instructions(),
        output_key="standard_project",
        sub_agents=[quality_assurance_sequence],
                generate_content_config=types.GenerateContentConfig(
            max_output_tokens=1000,
            temperature=1.0,
            safety_settings=DEFAULT_SAFETY_SETTINGS,
        ),
    )

root_agent = get_quality_assurance_coordinator_agent()