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
    from google.genai import types
    from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
    from google.adk.models.google_llm import Gemini
    from google.adk.runners import InMemoryRunner
    from google.adk.tools import AgentTool, FunctionTool, google_search

    retry_config = types.HttpRetryOptions(
            attempts=4,  # Maximum retry attempts
            exp_base=7,  # Delay multiplier
            initial_delay=1,
            http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
        )
    return (
        Gemini,
        InMemoryRunner,
        LlmAgent,
        ParallelAgent,
        SequentialAgent,
        google_search,
        mo,
        retry_config,
    )


@app.cell
def _(mo):
    mo.md("""
    ## QA Team ideas
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    Mulling these ideas over

    - Safety agent
    - clarity
    - spelling/grammar
    -
    """)
    return


@app.cell
def _(Gemini, LlmAgent, ParallelAgent, google_search, retry_config):
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

    # root_agent = LlmAgent(
    #         name="CraftSystemCoordinator",
    #         model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    #         instruction="""You are a craft research coordinator for
    #         parents and caregivers. You help find projects to
    #         do with toddlers that are safe. You ONLY help with
    #         safe toddler projects.

    #         Your goal is to answer the user's query by orchestating
    #         a workflow.
    #         1. First, you MUST call the related tools
    #         to find the relevant information on the topic provided
    #         by the user.
    #         2. Pick the safest, most detailed craft if presented with
    #         multiple options. If a user doesn't have a specific
    #         craft in mind - pick one of the options.
    #         3. Finally, present the final summary clearly to the
    #         user as your response.
    #         """,
    #         tools=[
    #             AgentTool(silly_craft_researcher),
    #         ],
    #)

    parallel_craft_team = ParallelAgent(
        name="CraftResearchTeam",
        sub_agents=[silly_craft_researcher, science_craft_researcher],
    )
    return (parallel_craft_team,)


@app.cell
def _(Gemini, LlmAgent, google_search, retry_config):
    safety_assurance = LlmAgent(
        name="SafetyAssuranceAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are an expert at assessing toddler safety.

        You will assess the safety of the following proposed
        toddler projects:

        **Silly Projects:** {silly_research}

        **Science Projects:** {science_research}

        You will provide your findings in a concise summary (100 words max)
        and REJECT OR APPROVE the project for human use.
        """,
        tools=[google_search],
        output_key="safety_report",
    )
    return (safety_assurance,)


@app.cell
def _(SequentialAgent, parallel_craft_team, safety_assurance):
    root_agent=SequentialAgent(
        name="ProjectRecommendation",
        sub_agents=[parallel_craft_team, safety_assurance]
    )
    return (root_agent,)


@app.cell
async def _(InMemoryRunner, root_agent):
    _runner = InMemoryRunner(agent=root_agent)
    _response = await _runner.run_debug(
        "Please recommend a silly project"
    )
    return


@app.cell
async def _(InMemoryRunner, root_agent):
    _runner = InMemoryRunner(agent=root_agent)
    _response = await _runner.run_debug(
        "Please recommend a dangerous project"
    )
    return


@app.cell
async def _(InMemoryRunner, root_agent):
    _runner = InMemoryRunner(agent=root_agent)
    _response = await _runner.run_debug(
        "Please recommend a silly project with knives"
    )
    return


@app.cell
async def _(InMemoryRunner, root_agent):
    _runner = InMemoryRunner(agent=root_agent)
    _response = await _runner.run_debug(
        "Please recommend a silly science project using water and sodium metal"
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
