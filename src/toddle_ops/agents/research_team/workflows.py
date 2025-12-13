from google.adk.agents import SequentialAgent
from toddle_ops.agents.research_team.agent import project_researcher, project_synthesizer

# Define the overall Research Pipeline as a Sequential Agent
research_sequence = SequentialAgent(
    name="ResearchSequence",
    sub_agents=[project_researcher, project_synthesizer],
)