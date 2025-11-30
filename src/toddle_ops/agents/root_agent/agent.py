from google.adk.agents import SequentialAgent, LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool

import toddle_ops.agents.craft_research_team.agent as craft
import toddle_ops.agents.quality_assurance_team.agent as qa

# import toddle_ops.agents.project_database_team.agent as db
from toddle_ops.config.basic import retry_config


project_pipeline = SequentialAgent(
    name="ToddleOpsSequence",
    sub_agents=[
        craft.root_agent,
        qa.root_agent,
    ],
)

root_agent = LlmAgent(
    name="ToddleOpsRoot",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
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

    - Output the project when the tool is finished.


    """,
    tools=[
        AgentTool(project_pipeline),
        # AgentTool(db.root_agent)
    ],
    output_key="project_request",
)
