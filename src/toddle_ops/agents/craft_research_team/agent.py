from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search
from google.adk.models.lite_llm import LiteLlm

from toddle_ops.config import retry_config
from toddle_ops.models.projects import Project

art_craft_researcher = LlmAgent(
    name="ArtCraftResearcher",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""
    Using google_search, research safe art crafts and projects
    for toddlers that are easy to do at home with
    common household materials. 

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
    Using google_search, research safe science-related crafts 
    and projects for toddlers that are easy to do at home with
    common household materials. 

    You WILL ONLY provide one project. Be sure to focus on
    the project name, duration, difficulty, required materials 
    and instructions.
    """,
    tools=[google_search],
    output_key="science_project",
)

# probably less of a parallel team and more as agent tools...
parallel_craft_team = ParallelAgent(
    name="CraftResearchTeam",
    sub_agents=[
        science_craft_researcher,
        art_craft_researcher,
    ],
)

project_synthesizer = LlmAgent(
    name="ProjectSynthesizer",
    model=LiteLlm(model="ollama_chat/gemma3:27b"),
    instruction="""You are a project synthesizer. You will receive research for
    multiple toddler projects from the CraftResearchTeam. 
    
    Your task is to analyze the research outputs and create a single, 
    coherent, sensible project. You can either pick the best project from the 
    provided research, or combine elements from them to create a new project.

    Research Outputs:
    - {art_project}
    - {science_project}

    Format should look like the following:

    **Name:** The name of the project
    **Description:** A brief 2-3 sentence description of the project
    **Duration:** The estimated duration of the project in minutes
    **Materials:** A bulleted list of materials required for the project
    **Instructions:** A numbered list of step-by-step instructions for the project

    There should be no extra categories or preamble or comments after
    the instructions.
    """,
    # output_schema=Project,
    output_key="standard_project",
)

# Your output MUST be a single `Project` object.
# prolly should separate the project schema out from this.
# one should be user facing, the other for future database manipulations

root_agent = SequentialAgent(
    name="CraftResearchPipeline",
    sub_agents=[parallel_craft_team, project_synthesizer],
)
