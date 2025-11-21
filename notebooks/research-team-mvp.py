# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "google-adk==1.19.0",
#     "protobuf==6.33.1",
# ]
# ///

import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    ## The Goal
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    I want a concierge type of agent team/service that will help me come up with novel, fun
    safe and educational crafts and projects I can do with my toddler.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Testing out some Agent MVPS
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Setup
    """)
    return


@app.cell
def _():
    # retry config
    from google.genai import types

    retry_config = types.HttpRetryOptions(
        attempts=4,  # Maximum retry attempts
        exp_base=7,  # Delay multiplier
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
    )
    return (retry_config,)


@app.cell
def _():
    from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
    from google.adk.models.google_llm import Gemini
    from google.adk.runners import InMemoryRunner
    from google.adk.tools import AgentTool, FunctionTool, google_search
    return (
        AgentTool,
        Gemini,
        InMemoryRunner,
        LlmAgent,
        ParallelAgent,
        google_search,
    )


@app.cell
def _(mo):
    mo.md("""
    ## parallel craft research team
    """)
    return


@app.cell
def _(Gemini, LlmAgent, google_search, retry_config):
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
    return (art_craft_researcher,)


@app.cell
def _(Gemini, LlmAgent, google_search, retry_config):
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
    return (science_craft_researcher,)


@app.cell
def _(Gemini, LlmAgent, google_search, retry_config):
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
    return (silly_craft_researcher,)


@app.cell
def _(
    ParallelAgent,
    art_craft_researcher,
    science_craft_researcher,
    silly_craft_researcher,
):
    parallel_craft_team = ParallelAgent(
        name="LookupTeam",
        sub_agents=[silly_craft_researcher, science_craft_researcher, art_craft_researcher],
    )
    return


@app.cell
def _(
    AgentTool,
    Gemini,
    LlmAgent,
    art_craft_researcher,
    retry_config,
    science_craft_researcher,
    silly_craft_researcher,
):
    root_agent = LlmAgent(
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
    return (root_agent,)


@app.cell
async def _(InMemoryRunner, root_agent):
    _runner = InMemoryRunner(agent=root_agent)
    _response = await _runner.run_debug("I need a silly craft")

    return


@app.cell
async def _(InMemoryRunner, root_agent):
    _runner = InMemoryRunner(agent=root_agent)
    _response = await _runner.run_debug("I need a science craft")
    return


@app.cell
async def _(InMemoryRunner, root_agent):
    _runner = InMemoryRunner(agent=root_agent)
    _response = await _runner.run_debug("I need an art craft")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
