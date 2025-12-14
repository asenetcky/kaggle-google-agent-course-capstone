from google.adk.apps import App
from google.adk.plugins.logging_plugin import LoggingPlugin

from toddle_ops.agents.orchestrator.agent import root_agent
from toddle_ops.config import events_compaction_config
from toddle_ops.plugins import error_handling_plugin

app = App(
    name="toddle_ops",
    root_agent=root_agent,
    events_compaction_config=events_compaction_config,
    plugins=[LoggingPlugin(), error_handling_plugin],
)
