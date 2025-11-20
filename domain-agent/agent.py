from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.google_search_tool import google_search

from google.genai import types
from typing import List

retry_config = types.HttpRetryOptions(
    attempts=5,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)


def pull_domain_metadata():
    pass

domain_pull_agent: LlmAgent = LlmAgent(
    name= "domain_pull_agent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    description="",
    instruction=""
    tools=[pull_domain_metadata]
)