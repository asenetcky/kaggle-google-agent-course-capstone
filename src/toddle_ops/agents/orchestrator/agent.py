import asyncio
from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import AgentTool, preload_memory

import toddle_ops.agents.craft_research_team.agent as craft
import toddle_ops.agents.quality_assurance_team.agent as qa
from toddle_ops.config import retry_config
from toddle_ops.models.projects import StandardProject
from toddle_ops.services.callbacks import auto_save_to_memory
from toddle_ops.models.agents import AgentInstructions

# project_formatter = LlmAgent(
#     name="ProjectFormatter",
#     model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
#     instruction="""You are a project formatter. You will receive a 
#     `StandardProject` object and your task is to format it into a human-readable
#     markdown format.

#     Here is the project data:
#     {standard_project}

#     There should be no extra categories or preamble or comments before or 
#     after the instructions.

#     Format should look like the following:
    
#     - **Name:** The name of the project

#     - **Description:** A brief 2-3 sentence description of the project

#     - **Duration:** The estimated duration of the project in minutes

#     - **Materials:** A bulleted list of materials required for the project

#     - **Instructions:** A numbered list of step-by-step instructions for the project
#     """,
#     input_schema=StandardProject,
#     output_key="human_project",
# )


formatter_instructions = AgentInstructions(
    persona="Project Formatter Agent",
    primary_objective=["Format StandardProject objects into human-readable markdown."],
    guiding_principles=[
        "Be concise and clear.",
        "Follow the specified format exactly.",
        "Ensure all required sections are included.",
        """
        Format should look like the following:
        
        - **Name:** The name of the project

        - **Description:** A brief 2-3 sentence description of the project

        - **Duration:** The estimated duration of the project in minutes

        - **Materials:** A bulleted list of materials required for the project

        - **Instructions:** A numbered list of step-by-step instructions for the project
        """,
    ],
    constraints=["There should be no extra categories or preamble or comments before or after the instructions"],
    incoming_keys=["standard_project"],
)


project_formatter = LlmAgent(
    name="ProjectFormatter",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=formatter_instructions.model_dump_json(),
    input_schema=StandardProject,
    output_key="human_project",
)

project_pipeline = SequentialAgent(
    name="ToddleOpsSequence",
    sub_agents=[
        craft.root_agent,
        qa.root_agent,
        project_formatter,
    ],
)

root_agent = LlmAgent(
    name="ToddleOpsRoot",
    model=LiteLlm(model="ollama_chat/mistral-nemo:12b"),
    # model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
    You are the root agent for ToddleOps.

    - Your PRIMARY purpose is to generate new projects for users based on their 
    requests using the `ToddleOpsSequence` tool you MUST use this tool for
    project requests.

    - You SHOULD NOT attempt to generate projects yourself without using this 
    tool.

    - If a user asks for a project with no details - do not prompt them for
    more details - just use the `ToddleOpsSequence` tool.

    - If they provide helpful details - pass that context on to the 
    `ToddleOpsSequence` tool.

    - ALWAYS Output the `human_project` when the tool is finished.


    """,
    tools=[
        AgentTool(project_pipeline),
        preload_memory,
    ],
    output_key="human_project",
    after_agent_callback=auto_save_to_memory,  # save after each turn
)

