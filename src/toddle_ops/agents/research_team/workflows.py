from google.adk.agents import SequentialAgent, ParallelAgent

from toddle_ops.agents.research_team.agent import (
    high_temp_project_researcher,
    low_temp_project_researcher,
    project_synthesizer,
)

research_parallel = ParallelAgent(
    name="ResearchParallel",
    sub_agents=[high_temp_project_researcher, low_temp_project_researcher],
)

# Define the overall Research Pipeline as a Sequential Agent
research_sequence = SequentialAgent(
    name="ResearchSequence",
    sub_agents=[research_parallel, project_synthesizer],
)
