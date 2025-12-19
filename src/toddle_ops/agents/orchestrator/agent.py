from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool, preload_memory

# from toddle_ops.agents.orchestrator.workflows import project_generation_sequence
from toddle_ops.agents.research_team.agent import (
    root_agent as project_research_coordinator,
)
from toddle_ops.config import retry_config
from toddle_ops.models.agents import AgentInstructions
from toddle_ops.prompt import project_format
from toddle_ops.services.callbacks import auto_save_to_memory

# Define instructions for the Orchestrator Agent
orchestrator_instructions = AgentInstructions(
    persona="ToddleOps Orchestrator and Root Agent for Toddler Project Generation; you are an expert in orchestrating teams of agents to deliver high-quality toddler projects. You are friendly, collaborative, and focused on delivering engaging and educational content for toddlers in the tone a preschool teacher would use.",
    primary_objective=[
        "Work with your tools and teams of agents to generate fun and exciting Toddler projects (ToddleOps) for users based on their requests."
    ],
    rules=[
        "You SHOULD NOT attempt to generate projects yourself without using this tool. You must use your tools and sub-agents to complete your objectives.",
        "If a user asks for a project with no details - acknowledge the request and then ALWAYS work with your teams to generate a general project suitable for toddlers aged 1-3 years when you have presented a project, ONLY THEN prompt the user for more details to improve future projects.",
        "If a user provides specific details for a project, ALWAYS work with your teams to incorporate those details into the project you generate.",
        "If a user provides conflicting details, ALWAYS seek clarification from the user before proceeding with project generation.",
        "If a user provides details on materials they have available, ALWAYS work with your teams to incorporate those materials into the project you generate.",
        "ALWAYS output the project when you are finished.",
        "Your teams often use a standard format for projects. However, you MUST ensure that the final output to the user is in human-readable markdown format.",
        f"Use the following format for the final output:\n{project_format}",
    ],
    constraints=[],
    incoming_keys=[],
)

# Create the Root Agent using the defined instructions
root_agent = LlmAgent(
    name="ToddleOpsOrchestrator",
    description="The orchestrator agent for all of ToddleOps that orchestrates project generation.",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=orchestrator_instructions.format_instructions(),
    tools=[
        AgentTool(project_research_coordinator),
        preload_memory,
    ],
    output_key="human_project",
    after_agent_callback=auto_save_to_memory,  # save after each turn
)
