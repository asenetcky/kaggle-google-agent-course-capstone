import asyncio
import time

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions.session import Session
from google.genai import types
from google.adk.agents.run_config import RunConfig

from toddle_ops.app import app
from toddle_ops.services.memory import memory_service
from toddle_ops.services.sessions import session_service

load_dotenv()  # load API keys and settings


async def main():

    user_id = "toddle_ops_user"
    runner = Runner(app=app, session_service=session_service, memory_service=memory_service)
    
    session: Session = await session_service.create_session(app_name=app.name, user_id=user_id)

    async def run_prompt(session: Session, new_message: str):
        content = types.Content(
            role='user', parts=[types.Part.from_text(text=new_message)]
        )
        print('** User says:', content.model_dump(exclude_none=True))
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=content,
        ):
          if event.content.parts and event.content.parts[0].text:
            print(f'** {event.author}: {event.content.parts[0].text}')


    start_time = time.time()
    print('Start time:', start_time)
    print('------------------------------------')

    await run_prompt(session, 'Hello ToddleOps! Please create a new project for me that you have no shared before,')

    end_time = time.time()
    print('------------------------------------')
    print('End time:', end_time)
    print('Total time:', end_time - start_time)


if __name__ == "__main__":
    asyncio.run(main())
