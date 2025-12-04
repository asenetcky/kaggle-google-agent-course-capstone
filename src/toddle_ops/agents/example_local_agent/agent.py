from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm

root_agent = Agent(
    model=LiteLlm(model="ollama_chat/qwen3:1.7b"),
    name="dice_agent",
    description=(
        "hello world agent that can roll a dice of 8 sides and check prime numbers."
    ),
    instruction="""
      You roll dice and answer questions about the outcome of the dice rolls.
    """,
)
