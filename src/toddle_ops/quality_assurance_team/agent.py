from google.adk.agents import LlmAgent, SequentialAgent, LoopAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import AgentTool, google_search, FunctionTool

import toddle_ops.craft_research_team.agent as craft
from toddle_ops.config.basic import retry_config

# Quality Assurance Loop

## helper functions
def exit_loop():
    """Call this function ONLY when the critique is 'APPROVED', indicating the
    project quality assurance process is finished and no more changes are
    needed."""
    return {
        "status": "approved",
        "message": "Project approved. Exiting Quality Assurance loop.",
    }

## Agents
initial_project_research = LlmAgent(
    name="InitialResearchAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config,
    ),
    description="Acts as entrypoint to QA loop .",
    # TODO: rewrite instuctions
    instruction="""You are a helpful concierge agent who aids parents and 
        caregivers engage in "ToddleOps" - the process of creating, 
        inventorying and  managing safe, educational and fun projects toddlers 
        and their caregivers can do from home or a safe space. 

        You have a team of agents and tools specialized in researching 
        projects, activities and crafts, as well as safety, editing to 
        ensure a highy quality experience for your end users.
        
        - You MUST use one or more of your AgentTools to provide a single
        high-quality Toddler project with description, material list and 
        instructions
        - ONLY provide a single project
        - You ONLY help with ToddlerOps, crafts and projects
        """,
    tools=[
        AgentTool(agent=craft.art_craft_researcher),
        AgentTool(agent=craft.science_craft_researcher),
        AgentTool(agent=craft.silly_craft_researcher),
        AgentTool(agent=craft.random_craft_researcher),
    ],
    output_key="current_project",
)

safety_report_agent = LlmAgent(
    name="SafetyReportAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are an expert at assessing toddler safety.

    You will assess the safety of the following proposed
    toddler project: {current_project}

    - You will provide your findings in a concise summary (100 words max)
    - If the project is deemed safe and appropriate, you MUST respond with
    the exact phrase: "APPROVED"
    - Otherwise, provide 2-3 specific, actionable suggestions for
    improving safety.
    """,
    #tools=[google_search],
    output_key="safety_report",
)

safety_critic_agent = LlmAgent(
    name="SafetyCriticAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""You are a project toddler safety specialist. You have a 
    draft toddler project and safety report.
    
    Draft Project: {current_project}
    Safety Report: {safety_report}
    
    Your task is to analyze the Safety Report.
    - IF the report is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
    - OTHERWISE, rewrite the draft project to fully incorporate the feedback 
    from the report.""",
    output_key="current_project",  # It overwrites the project with the new, safer version.
    tools=[
       # google_search,
        FunctionTool(exit_loop)
    ],  
)


# testing
# safety_loop = LoopAgent(
#     name="SafetyLoop",
#     sub_agents=[safety_report_agent,safety_critic_agent],
#     max_iterations=2,
# )

# root_agent = SequentialAgent(
#     name="SafetyPipeline",
#     sub_agents=[initial_project_research, safety_loop],
# )


# from dotenv import load_dotenv
# # Load environment variables from .env
# try:
#     load_dotenv()
#     GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
# except Exception as e:
#     print(f"Auth error: Details: {e}")


# from google.adk.runners import InMemoryRunner

# runner = InMemoryRunner(agent=root_agent)
# response = await runner.run_debug(
#     "Please provide me with a random toddler project :)"
# )




clarity_editor = LlmAgent(
    name="ClarityEditor",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are an expert editor.

    Review the following project description for clarity.
    Ensure the instructions are easy to understand for a parent or caregiver.
    Rewrite the project description to improve clarity if necessary.

    **Project Description:** {silly_research}
    """,
    output_key="clarity_edited_project",
)

grammar_spelling_editor = LlmAgent(
    name="GrammarSpellingEditor",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are an expert proofreader.

    Review the following project description for spelling and grammar errors.
    Correct any spelling or grammar mistakes.

    **Project Description:** {clarity_edited_project}
    """,
    output_key="final_draft",
)


editorial_team = SequentialAgent(
    name="EditorialTeam",
    sub_agents=[clarity_editor, grammar_spelling_editor],
)

project_approver = LlmAgent(
    name="ProjectApprover",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are an expert at assessing toddler safety.

    You will assess the safety of the following proposed
    toddler projects:

    **Safety Report:** {safety_report}

    You will provide your findings in a concise summary (100 words max)
    and respond with "APPROVE" or "REJECT".
    """,
    output_key="verdict",
)


router = LlmAgent(
    name="Router",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""Given the verdict, decide the next step.
    If the verdict is 'APPROVE', call the 'editorial_team' with the project description.
    If the verdict is 'REJECT', just output the safety report.

    **Verdict:** {verdict}
    **Project Description:** {silly_research}
    **Safety Report:** {safety_report}
    """,
    tools=[AgentTool(editorial_team)],
    output_key="final_output",
)
