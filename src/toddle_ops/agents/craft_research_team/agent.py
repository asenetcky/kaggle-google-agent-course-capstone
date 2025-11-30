from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from toddle_ops.config.basic import retry_config
from toddle_ops.models.projects import Project

art_craft_researcher = LlmAgent(
    name="ArtCraftResearcher",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
    Research popular and safe art crafts and projects
    for toddlers that are easy to do at home with
    common household materials. 
    tou WILL ONLY provide one project.

    You WILL ONLY provide one project. Be sure to focus on
    the project name, duration, difficulty, required materials 
    and instructions.
    """,
    tools=[google_search],
    output_key="art_project",
)

science_craft_researcher = LlmAgent(
    name="ScienceCraftResearcher",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
    Research popular and safe science-related crafts
    or projects for toddlers that are easy to do at home with
    common household materials. 

    You WILL ONLY provide one project. Be sure to focus on
    the project name, duration, difficulty, required materials 
    and instructions.
    """,
    tools=[google_search],
    output_key="science_project",
)

silly_craft_researcher = LlmAgent(
    name="SillyCraftResearcher",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
    Research popular and safe silly crafts or projects
    for toddlers that are easy to do at home with
    common household materials.

    You WILL ONLY provide one project. Be sure to focus on
    the project name, duration, difficulty, required materials 
    and instructions.
    """,
    tools=[google_search],
    output_key="silly_project",
)


random_craft_researcher = LlmAgent(
    name="RandomCraftResearcher",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
    Research random crafts or projects
    for toddlers that are easy to do at home with
    common household materials.

    You WILL ONLY provide one project. Be sure to focus on
    the project name, duration, difficulty, required materials 
    and instructions.
    """,
    tools=[google_search],
    output_key="random_project",
)

# probably less of a parallel team and more as agent tools...
parallel_craft_team = ParallelAgent(
    name="CraftResearchTeam",
    sub_agents=[
        # silly_craft_researcher,
        science_craft_researcher,
        art_craft_researcher,
        # random_craft_researcher,
    ],
)

# removing some parallel agents for billing purposes :D
# also a bit redundant
# removing:
#    - {silly_project}
#    - {random_project}

project_synthesizer = LlmAgent(
    name="ProjectSynthesizer",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are a project synthesizer. You will receive research for
    multiple toddler projects from the CraftResearchTeam. 
    
    Your task is to analyze the research outputs and create a single, 
    sensible project. You can either pick the best project from the 
    provided research, or combine elements from them to create a new project.

    Research Outputs:

    - {art_project}
    - {science_project}

    Your output MUST be a single `Project` object.
    """,
    output_schema=Project,
    output_key="standard_project",
)

root_agent = SequentialAgent(
    name="CraftResearchPipeline",
    sub_agents=[parallel_craft_team, project_synthesizer],
)
