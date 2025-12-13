from google.adk.agents import SequentialAgent, LoopAgent
from toddle_ops.agents.quality_assurance_team.agent import  editorial_agent, safety_critic_agent, safety_refiner_agent

# Workflows for Quality Assurance Team Agents

# Define the Safety Refinement Loop as a Loop Agent
safety_refinement_loop = LoopAgent(
    name="SafetyRefinementLoop",
    sub_agents=[safety_critic_agent, safety_refiner_agent],
    max_iterations=1,
)

# Define the overall Quality Assurance Sequence as a Sequential Agent
quality_assurance_sequence = SequentialAgent(
    name="QualityAssuranceSequence",
    sub_agents=[safety_refinement_loop, editorial_agent],
)
