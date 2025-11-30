import os
from dotenv import load_dotenv

from google.adk.apps.app import App

from toddle_ops.agents.root_agent.agent import root_agent
from toddle_ops.config.basic import events_compaction_config

# Load environment variables from .env
try:
    load_dotenv()
    GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
except Exception as e:
    print(f"Auth error: Details: {e}")

APP_NAME = "default"  # Application
USER_ID = "default"  # User
SESSION = "default"  # Session

MODEL_NAME = "gemini-2.5-flash-lite"

adk_app = App(
    name=APP_NAME,
    root_agent=root_agent,
    events_compaction_config=events_compaction_config,
)
