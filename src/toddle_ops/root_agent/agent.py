from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool

from toddle_ops.config.basic import retry_config
import toddle_ops.craft_research_team.agent as craft

root_agent = LlmAgent(
    name="ToddleOpsCoordinator",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config,
    ),
    description="Acts as entrypoint - coordinating toddleops with users.",
    instruction="""You are a helpful concierge agent who aids parents and caregivers 
        engage in "ToddleOps" - the process of creating, inventorying and 
        managing safe, educational and fun projects toddlers and their 
        caregivers can do from home or a safe space. 

        You have a team of agents and tools specialized in researching 
        projects, activities and crafts, as well as safety, editing to 
        ensure a highy quality experience for your end users.
        
        - You MUST use one or more of your AgentTools to provide the project
        description, material list and instructions
        - You ONLY help with ToddlerOps, crafts and projects
        """,
    tools=[
        AgentTool(agent=craft.art_craft_researcher),
        AgentTool(agent=craft.science_craft_researcher),
        AgentTool(agent=craft.silly_craft_researcher),
    ],
)
