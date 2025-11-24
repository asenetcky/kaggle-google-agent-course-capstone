import asyncio
import os

from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner

from toddle_ops.root_agent.agent import root_agent

# Load environment variables from .env
try:
    load_dotenv()
    GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
except Exception as e:
    print(f"Auth error: Details: {e}")


async def main() -> None:
    runner = InMemoryRunner(agent=root_agent)
    response = await runner.run_debug("provide a art project to do with my toddler")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
