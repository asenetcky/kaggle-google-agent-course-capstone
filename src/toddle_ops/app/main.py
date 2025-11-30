from dotenv import load_dotenv
import asyncio
from google.adk.cli.utils import logs
from google.adk.runners import InMemoryRunner

from toddle_ops.services.sessions import session_service
from toddle_ops.services.memory import memory_service
from toddle_ops.services.callbacks import auto_save_to_memory
from toddle_ops.agents.root_agent.agent import root_agent

load_dotenv()
logs.log_to_tmp_folder()


APP_NAME = "toddle_ops"

runner = InMemoryRunner(
        root_agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
        memory_service=memory_service,
    )

async def main():
    try:
        _response = await runner.run_debug("Hello - I would like a project.")
    except Exception as e:
        print(f"An error occurred during toddle ops execution: {e}")

if __name__ == "__main__":
    asyncio.run(main())

