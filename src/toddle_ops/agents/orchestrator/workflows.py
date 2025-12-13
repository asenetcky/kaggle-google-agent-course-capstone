from google.adk.agents import SequentialAgent
import toddle_ops.agents.research_team.workflows as craft
import toddle_ops.agents.quality_assurance_team.workflows as qa
from toddle_ops.agents.orchestrator.agent import project_formatter

# Define the overall project pipeline as a Sequential Agent
project_generation_sequence = SequentialAgent(
    name="ProjectGenerationSequence",
    sub_agents=[
        craft.research_sequence,
        qa.quality_assurance_sequence,
        project_formatter,
    ],
)