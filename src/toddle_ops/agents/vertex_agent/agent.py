import os

import vertexai
from dotenv import load_dotenv

import toddle_ops.agents.root_agent.agent as root

# Load environment variables from .env

try:
    load_dotenv()
    vertexai.init(
        project=os.environ["GOOGLE_CLOUD_PROJECT"],
        location=os.environ["GOOGLE_CLOUD_LOCATION"],
    )
except Exception as e:
    print(f"Auth error: Details: {e}")

root_agent = root.root_agent
