import asyncio
import logging

from dotenv import load_dotenv
from google.adk.runners import Runner

from toddle_ops.local_app.agent import adk_app
from toddle_ops.services.memory import memory_service
from toddle_ops.services.sessions import session_service

load_dotenv()

logging.basicConfig(
    filename="logger.log",
    level=logging.WARNING,
    format="'%(asctime)s - %(levelname)s - %(name)s - %(message)s'",
)

APP_NAME = "toddle_ops"

runner = Runner(
    app=adk_app,
    session_service=session_service,
    memory_service=memory_service,
)


async def main():
    try:
        _response = await runner.run_debug("Please provide a project.")
    except Exception as e:
        print(f"An error occurred during toddle ops execution: {e}")


if __name__ == "__main__":
    asyncio.run(main())
