# Save Session to memory automatically
# intended for use at the end of a conversation - batch processing/ reduce api calls
async def auto_save_to_memory(callback_context):
    """Automatically save session to memory after each agent turn."""
    # Check if memory service is available (it may be None when running via CLI)
    memory_service = callback_context._invocation_context.memory_service
    if memory_service is not None:
        await memory_service.add_session_to_memory(
            callback_context._invocation_context.session
        )
