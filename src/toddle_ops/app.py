from toddle_ops.agents.orchestrator.agent import root_agent

from google.adk.apps import App

app = App(
    name="toddle_ops", 
    root_agent=root_agent,
)