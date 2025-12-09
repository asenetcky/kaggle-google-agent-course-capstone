from google.adk.tools.tool_context import ToolContext
from pydantic import BaseModel

from toddle_ops.enums import Status


# TODO add description annotations etc...
class ActionReport(BaseModel):
    status: Status
    message: str | None
    tool_context: ToolContext | None
