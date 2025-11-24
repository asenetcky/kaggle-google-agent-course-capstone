from google.adk.agents import LlmAgent, SequentialAgent
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
        AgentTool(agent=craft.random_craft_researcher),
    ],
    output_key="current_project",
)

safety_assurance = LlmAgent(
    name="SafetyAssuranceAgent",
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
    tools=[google_search],
    output_key="safety_report",
)

safety_agent = LlmAgent(
    name="SafetyAgent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    instruction="""You are a project toddler safety specialist. You have a 
    draft toddler project and safety report.
    
    Draft Project: {current_story}
    Safety Report: {critique}
    
    Your task is to analyze the Safety Report.
    - IF the report is EXACTLY "APPROVED", you MUST call the `exit_loop` function and nothing else.
    - OTHERWISE, rewrite the draft project to fully incorporate the feedback 
    from the report.""",
    output_key="current_project",  # It overwrites the project with the new, safer version.
    tools=[
        google_search,
        FunctionTool(exit_loop)
    ],  
)





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
