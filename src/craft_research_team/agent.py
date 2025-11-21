from google.adk.agents import LlmAgent, ParallelAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from craft_research_team.config import retry_config

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

parallel_craft_team = ParallelAgent(
    name="CraftResearchTeam",
    sub_agents=[silly_craft_researcher, science_craft_researcher, art_craft_researcher],
)
