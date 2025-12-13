from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool, preload_memory

from toddle_ops.config import retry_config
from toddle_ops.services.callbacks import auto_save_to_memory
from toddle_ops.models.agents import AgentInstructions
from toddle_ops.agents.orchestrator.workflows import project_generation_sequence


# Define instructions for the Root Agent
root_agent_instructions = AgentInstructions(
    persona="ToddleOps Root Agent",
    primary_objective=["Generate new projects for users based on their requests using the `ToddleOpsSequence` tool."],
    rules=[
        "Your PRIMARY purpose is to generate new projects for users based on their requests using the `ToddleOpsSequence` tool you MUST use this tool for project requests.",
        "You SHOULD NOT attempt to generate projects yourself without using this tool.",
        "If a user asks for a project with no details - do not prompt them for more details - just use the `ToddleOpsSequence` tool.",
        "If they provide helpful details - pass that context on to the `ToddleOpsSequence` tool.",
        "ALWAYS Output the `human_project` when the tool is finished.",
    ],
    constraints=[],
    incoming_keys=[],
)

# Create the Root Agent using the defined instructions
root_agent = LlmAgent(
    name="ToddleOpsRoot",
    description="The root agent for all of ToddleOps that orchestrates project generation.",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=root_agent_instructions.format_instructions(),
    tools=[
        AgentTool(project_generation_sequence),
        preload_memory,
    ],
    output_key="human_project",
    after_agent_callback=auto_save_to_memory,  # save after each turn
)

