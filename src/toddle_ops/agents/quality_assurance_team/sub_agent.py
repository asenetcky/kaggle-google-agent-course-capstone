from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

from toddle_ops.agents.factory import create_agent
from toddle_ops.helpers import exit_loop
from toddle_ops.models.agents import AgentInstructions
from toddle_ops.models.reports import StatusReport


# Define instructions for the Safety Critic Agent
safety_critic_instructions = AgentInstructions(
    persona="Toddler Safety Critic",
    primary_objective=[
        "Assess the safety of toddler projects to ensure they are appropriate and safe for children aged 1-3 years."
    ],
    rules=[
        "Provide a direct, and concise summary of your findings.",
        "If the project is safe, set status in the StatusReport to 'Status.APPROVED'.",
        "If the project is not safe, set status in the StatusReport to 'Status.REVISION_NEEDED' and provide specific, actionable suggestions.",
    ],
    constraints=[],
    incoming_keys=["standard_project"],
)

# Create the Safety Critic Agent using the defined instructions
def get_safety_critic_agent() -> LlmAgent:
    """Create a Safety Critic agent that evaluates project safety."""
    return create_agent(
        name="SafetyCriticAgent",
        description="Evaluates toddler projects for safety and provides feedback.",
        instruction=safety_critic_instructions.format_instructions(),
        output_schema=StatusReport,
        output_key="safety_report",
    )

# Define instructions for the Safety Refiner Agent
safety_refiner_instructions = AgentInstructions(
    persona="Toddler Safety Refiner",
    primary_objective=[
        "Revise toddler projects based on safety feedback to ensure they are safe and appropriate for children aged 1-3 years."
    ],
    rules=[
        "If the safety report status is 'APPROVED', call the `exit_loop` function and do nothing else.",
        "If the status is 'REVISION_NEEDED', carefully incorporate the feedback into the project.",
        "Ensure the revised project maintains clarity and age-appropriateness.",
    ],
    constraints=[],
    incoming_keys=["standard_project", "safety_report"],
)

# todo: implement tool that consumes ActionReport with logic based around status.
# Define the Safety Refiner Agent using the defined instructions
def get_safety_refiner_agent() -> LlmAgent:
    """Create a Safety Refiner agent that revises projects based on feedback."""
    return create_agent(
        name="SafetyRefinerAgent",
        description="Refines toddler projects based on safety feedback.",
        instruction=safety_refiner_instructions.format_instructions(),
        output_key="standard_project",  # It overwrites the project with the new, safer version.
        tools=[FunctionTool(exit_loop)],
    )

# Define instructions for the Editorial Agent
editorial_instructions = AgentInstructions(
    persona="Editorial Agent",
    primary_objective=[
        "Edit and proofread toddler projects to ensure clarity, age-appropriateness, and correctness."
    ],
    rules=[
        "Check for clarity, age-appropriateness, spelling, and grammar.",
        "Projects are meant for children aged 1-3 years, accompanied by an adult.",
        "Ensure the instructions are easy for a parent or caregiver to understand.",
        "Correct all spelling and grammar mistakes.",
        "Rewrite the project to improve clarity and correctness where necessary.",
        "The final output should only correct the project content, maintaining the original format.",
    ],
    constraints=[],
    incoming_keys=["standard_project"],
)

def get_editorial_agent() -> LlmAgent:
    """Create an Editorial agent that proofreads projects."""
    return create_agent(
        name="EditorialAgent",
        description="Edits and proofreads toddler projects for clarity and correctness.",
        instruction=editorial_instructions.format_instructions(),
        output_key="standard_project",
    )
