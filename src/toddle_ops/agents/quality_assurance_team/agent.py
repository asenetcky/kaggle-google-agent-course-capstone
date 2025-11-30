from google.adk.agents import LlmAgent, LoopAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool

from toddle_ops.config.basic import retry_config
from toddle_ops.models.projects import SafetyReport

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

### safety loop
safety_critic_agent = LlmAgent(
    name="SafetyCriticAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are an expert at assessing toddler safety.

    You will assess the safety of the following proposed
    toddler project: {standard_project}

    - You will provide your findings in a concise summary.
    - If the project is deemed safe and appropriate, your status MUST be 'APPROVED'.
    - Otherwise, your status MUST be 'NEEDS_REVISION', and you must provide
      specific, actionable suggestions for improving safety.
    - Your output must be a `SafetyReport` object.
    """,
    output_schema=SafetyReport,
    output_key="safety_report",
)

safety_refiner_agent = LlmAgent(
    name="SafetyRefinerAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are a project toddler safety specialist. You have a 
    draft toddler project and safety report.
    
    Draft Project: {standard_project}
    Safety Report: {safety_report}
    
    Your task is to analyze the Safety Report.
    - IF the report's status is 'APPROVED', you MUST call the `exit_loop` function and nothing else.
    - OTHERWISE, rewrite the draft project to fully incorporate the feedback 
    from the report.""",
    output_key="current_project",  # It overwrites the project with the new, safer version.
    tools=[FunctionTool(exit_loop)],
)

safety_refinement_loop = LoopAgent(
    name="ToddleOpsSafetyLoop",
    sub_agents=[safety_critic_agent, safety_refiner_agent],
    max_iterations=2,
)


### editor loop
editorial_agent = LlmAgent(
    name="EditorialAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are an expert editor and proofreader.

    Review the following project for clarity, age-appropriateness, spelling, and grammar.
    - Projects are meant for children aged 1-3 years, accompanied by an adult.
    - Ensure the instructions are easy for a parent or caregiver to understand.
    - Correct all spelling and grammar mistakes.
    - Rewrite the project to improve clarity and correctness where necessary.

    The final output should only correct the project content, maintaining the original format.

    **Project:** {standard_project}
    """,
    output_key="standard_project",
)

root_agent = SequentialAgent(
    name="QualityAssurancePipeline",
    sub_agents=[safety_refinement_loop, editorial_agent],
)
