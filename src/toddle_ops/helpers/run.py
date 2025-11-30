from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


async def run_session(
    runner_instance: Runner,
    session_service: InMemorySessionService,
    user_queries: list[str] | str = None,
    session_name: str = "default",
    app_name: str = "default",
    user_id: str = "default",
    model_name: str = "gemini-2.5-flash-lite",
):
    print(f"\n ### Session: {session_name}")

    # Get app name from the Runner
    app_name = runner_instance.app_name

    # Attempt to create a new session or retrieve an existing one
    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=user_id, session_id=session_name
        )
    except:  # noqa: E722
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_name
        )

    # Process queries if provided
    if user_queries:
        # Convert single query to list for uniform processing
        if type(user_queries) == str:  # noqa: E721
            user_queries = [user_queries]

        # Process each query in the list sequentially
        for query in user_queries:
            print(f"\nUser > {query}")

            # Convert the query string to the ADK Content format
            query = types.Content(role="user", parts=[types.Part(text=query)])

            # Stream the agent's response asynchronously
            async for event in runner_instance.run_async(
                user_id=user_id, session_id=session.id, new_message=query
            ):
                # Check if the event contains valid content
                if event.content and event.content.parts:
                    # Filter out empty or "None" responses before printing
                    if (
                        event.content.parts[0].text != "None"
                        and event.content.parts[0].text
                    ):
                        print(f"{model_name} > ", event.content.parts[0].text)
    else:
        print("No queries!")
