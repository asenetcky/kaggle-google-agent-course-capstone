from google.adk.apps.app import App
from google.adk.plugins import ReflectAndRetryToolPlugin

from toddle_ops.enums import Status
from toddle_ops.models.reports import StatusReport


class CustomRetryPlugin(ReflectAndRetryToolPlugin):
    async def extract_error_from_result(self, *, tool, tool_args, tool_context, result):
        # Detect error based on response content
        # Check if result is a StatusReport Pydantic model
        if isinstance(result, StatusReport):
            # StatusReport doesn't represent errors, it's used for workflow status
            # Only treat REJECTED status as an error that needs retry
            if result.status == Status.REJECTED:
                return result
            return None
        # Check if result is a dictionary (for backward compatibility)
        if isinstance(result, dict) and result.get("status") == "error":
            return result
        return None  # No error detected


# add this modified plugin to your App object:
error_handling_plugin = CustomRetryPlugin(max_retries=2)
