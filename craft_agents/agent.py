from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from craft_agents.config import retry_config

from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, FunctionTool, google_search
from google.genai import types


safety_officer = ""
aggregator = ""
material_researcher = ""

art_craft_researcher = LlmAgent(
    name="ArtCraftResearcher",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
    Research popular and safe art crafts and projects
    for toddlers that are easy to do at home with
    common household materials. 

    Return detailed step-by-step instructions
    of the activity for parents and caregivers
    and a bulleted material list.
    """,
    tools=[google_search],
    output_key="art_research",
)

science_craft_researcher = LlmAgent(
    name="ScienceCraftResearcher",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
    Research popular and safe science-related crafts
    or projects for toddlers that are easy to do at home with
    common household materials.

    Return detailed step-by-step instructions
    of the activity for parents and caregivers
    and a bulleted material list.
    """,
    tools=[google_search],
    output_key="science_research",
)


silly_craft_researcher = LlmAgent(
    name="SillyCraftResearcher",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
    Research popular and safe silly crafts or projects
    for toddlers that are easy to do at home with
    common household materials.

    Return detailed step-by-step instructions
    of the activity for parents and caregivers
    and a bulleted material list.
    """,
    tools=[google_search],
    output_key="silly_research",
)


# do a human in the loop to select which craft they want

polisher = ""
aggregator = ""

# right now for testing
polish_team = LlmAgent()


parallel_craft_team = ParallelAgent(
    name="LookupTeam",
    sub_agents=[silly_craft_researcher, science_craft_researcher, art_craft_researcher],
)

test_root_agent = LlmAgent(
    name="CraftSystemCoordinator",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are a craft research coordinator for
    parents and caregivers. You help find projects to
    do with toddlers that are safe. You ONLY help with
    safe toddler projects.

    Your goal is to answer the user's query by orchestating
    a workflow.
    1. First, you MUST call the related tools
    to find the relevant information on the topic provided
    by the user.
    2. Pick the safest, most detailed craft if presented with
    multiple options. If a user doesn't have a specific
    craft in mind - pick one of the options.
    3. Finally, present the final summary clearly to the
    user as your response.
    """,
    tools=[
        AgentTool(silly_craft_researcher),
        AgentTool(science_craft_researcher),
        AgentTool(art_craft_researcher),
    ],
)

async def test():
    runner = InMemoryRunner(agent=test_root_agent)
    response = await runner.run_debug(
    "I need a science craft"
    )
    return response

await test()

root_agent = SequentialAgent(
    name="CraftSystem",
    sub_agents=[
        parallel_craft_team,
        polish_team,
    ],
)
