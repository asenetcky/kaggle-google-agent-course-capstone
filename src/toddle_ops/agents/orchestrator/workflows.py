from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.models.google_llm import Gemini
import toddle_ops.agents.research_team.workflows as craft
import toddle_ops.agents.quality_assurance_team.workflows as qa
from toddle_ops.config import retry_config
from toddle_ops.models.projects import StandardProject
from toddle_ops.models.agents import AgentInstructions

# Define instructions for the Project Formatter Agent
formatter_instructions = AgentInstructions(
    persona="Project Formatter Agent",
    primary_objective=["Format StandardProject objects into human-readable markdown."],
    rules=[
        "Be concise and clear.",
        "Follow the specified format exactly.",
        "Ensure all required sections are included.",
        """
        Format should look like the following:
        
        - **Name:** The name of the project

        - **Description:** A brief 2-3 sentence description of the project

        - **Duration:** The estimated duration of the project in minutes

        - **Materials:** A bulleted list of materials required for the project

        - **Instructions:** A numbered list of step-by-step instructions for the project
        """,
    ],
    constraints=["There should be no extra categories or preamble or comments before or after the instructions"],
    incoming_keys=["standard_project"],
)

# Create the Project Formatter Agent using the defined instructions
project_formatter = LlmAgent(
    name="ProjectFormatter",
    description="Formats StandardProject objects into human-readable markdown.",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=formatter_instructions.format_instructions(),
    input_schema=StandardProject,
    output_key="human_project",
)

# Define the overall project pipeline as a Sequential Agent
project_generation_sequence = SequentialAgent(
    name="ProjectGenerationSequence",
    sub_agents=[
        craft.research_sequence,
        qa.quality_assurance_sequence,
        project_formatter,
    ],
)