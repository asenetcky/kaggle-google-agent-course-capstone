from dotenv import load_dotenv
import asyncio
import logging
from google.adk.runners import Runner

from toddle_ops.services.sessions import session_service
from toddle_ops.services.memory import memory_service
from toddle_ops.app.agent import adk_app

load_dotenv()

logging.basicConfig(
    filename="logger.log",
    level=logging.INFO,
    # format="%(filename)s:%(lineno)s %(levelname)s:%(message)s",
    format="'%(asctime)s - %(levelname)s - %(name)s - %(message)s'",
)

APP_NAME = "toddle_ops"

runner = Runner(
    # agent=root_agent,
    app=adk_app,
    # app_name=APP_NAME,
    session_service=session_service,
    memory_service=memory_service,
)


async def main():
    try:
        _response = await runner.run_debug(
            "Hello - I would like a toddler project please."
        )
    except Exception as e:
        print(f"An error occurred during toddle ops execution: {e}")


if __name__ == "__main__":
    asyncio.run(main())
