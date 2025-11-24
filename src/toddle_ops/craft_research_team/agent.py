from google.adk.agents import LlmAgent, ParallelAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from toddle_ops.config.basic import retry_config

art_craft_researcher = LlmAgent(
    name="ArtCraftResearcher",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
    Research popular and safe art crafts and projects
    for toddlers that are easy to do at home with
    common household materials. 

    You WILL ONLY use the following format:

    **Project Name:** Name of Project

    **Description:** Concise 2-3 sentence description of project

    **Materials:** A bulleted list of required materials

    **Instructions:** Enumerated step-by-step instructions that
    are easy to read and understand for parents and caregivers.
    """,
    tools=[google_search],
    output_key="project_research",
)

science_craft_researcher = LlmAgent(
    name="ScienceCraftResearcher",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
    Research popular and safe science-related crafts
    or projects for toddlers that are easy to do at home with
    common household materials.

    You WILL ONLY use the following format:

    **Project Name:** Name of Project

    **Description:** Concise 2-3 sentence description of project

    **Materials:** A bulleted list of required materials

    **Instructions:** Enumerated step-by-step instructions that
    are easy to read and understand for parents and caregivers.
    """,
    tools=[google_search],
    output_key="project_research",
)

silly_craft_researcher = LlmAgent(
    name="SillyCraftResearcher",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
    Research popular and safe silly crafts or projects
    for toddlers that are easy to do at home with
    common household materials.

    You WILL ONLY use the following format:

    **Project Name:** Name of Project

    **Description:** Concise 2-3 sentence description of project

    **Materials:** A bulleted list of required materials

    **Instructions:** Enumerated step-by-step instructions that
    are easy to read and understand for parents and caregivers.
    """,
    tools=[google_search],
    output_key="project_research",
)


random_craft_researcher = LlmAgent(
    name="RandomCraftResearcher",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
    Research random crafts or projects
    for toddlers that are easy to do at home with
    common household materials.

    You WILL ONLY use the following format:

    **Project Name:** Name of Project

    **Description:** Concise 2-3 sentence description of project

    **Materials:** A bulleted list of required materials

    **Instructions:** Enumerated step-by-step instructions that
    are easy to read and understand for parents and caregivers.
    """,
    tools=[google_search],
    output_key="project_research",
)

# probably less of a parallel team and more as agent tools...
parallel_craft_team = ParallelAgent(
    name="CraftResearchTeam",
    sub_agents=[silly_craft_researcher, science_craft_researcher, art_craft_researcher],
)
