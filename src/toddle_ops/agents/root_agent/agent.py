from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool, preload_memory
from google.adk.models.lite_llm import LiteLlm

import toddle_ops.agents.craft_research_team.agent as craft
import toddle_ops.agents.quality_assurance_team.agent as qa
from toddle_ops.config import retry_config, events_compaction_config
from toddle_ops.services.callbacks import auto_save_to_memory

project_pipeline = SequentialAgent(
    name="ToddleOpsSequence",
    sub_agents=[
        craft.root_agent,
        qa.root_agent,
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

    - If a user asks for a project - you MUST provide a project, do not 
    request more details.

    """,
    tools=[
        AgentTool(project_pipeline),
        preload_memory,
    ],
    after_agent_callback=auto_save_to_memory,  # save after each turn
)

# from google.adk.apps import App

# # my_app = App(
# #     name = "app",
# #     root_agent=root_agent,
# #     events_compaction_config=events_compaction_config
# # )

# from google.adk.runners import Runner
# from toddle_ops.services.memory import memory_service
# from toddle_ops.services.sessions import session_service

# runrun = Runner(
#     agent=root_agent,
#     app_name="upgrade_synthesizer",
#     session_service=session_service,
#     memory_service=memory_service,
# )

# await runrun.run_debug("I would like an art project - any project will do.")
