from google.adk.agents import LlmAgent, LoopAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import FunctionTool

from toddle_ops.config import retry_config
from toddle_ops.helpers import exit_loop
from toddle_ops.models.actions import ActionReport

# Quality Assurance Loop

## Agents
### safety loop
safety_critic_agent = LlmAgent(
    name="SafetyCriticAgent",
    # model=LiteLlm(model="ollama_chat/gemma3:27b"),
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are an expert at assessing toddler safety.

    You will assess the safety of the following proposed
    toddler project: {standard_project}

    - You will provide your findings in a concise summary inside of 'message'
        in the ActionReport.
    - If the project is deemed safe and appropriate, your status MUST be 
        'Status.APPROVED'.
    - Otherwise, your status MUST be 'Status.REVISION_NEEDED', and you must 
        provide specific, actionable suggestions for improving safety in 
        the ActionReport.
    - Your output must be a  ActionReport object.
    """,
    output_schema=ActionReport,
    output_key="safety_report",
)

# todo: implement tool that consumes ActionReport with logic based around status.

safety_refiner_agent = LlmAgent(
    name="SafetyRefinerAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction="""You are a project toddler safety specialist. You have a 
    draft toddler project and safety report.
    
    Draft Project: {standard_project}
    Safety Report: {safety_report}
    
    Your task is to analyze the Safety Report.
    - IF the safety_report's status is 'APPROVED', you MUST call the `exit_loop` function and nothing else.
    - OTHERWISE, rewrite the draft project to fully incorporate the feedback 
        from the report.
    Your output MUST be a `StandardProject` object.""",
    output_key="standard_project",  # It overwrites the project with the new, safer version.
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

    Review the following project:
        {standard_project}

    for the following:

    - clarity, age-appropriateness, spelling, and grammar.
    - Projects are meant for children aged 1-3 years, accompanied by an adult.
    - Ensure the instructions are easy for a parent or caregiver to understand.
    - Correct all spelling and grammar mistakes.
    - Rewrite the project to improve clarity and correctness where necessary.

    The final output should only correct the project content, 
    maintaining the original format.

    """,
    output_key="standard_project",
)

root_agent = SequentialAgent(
    name="QualityAssurancePipeline",
    sub_agents=[safety_refinement_loop, editorial_agent],
)
