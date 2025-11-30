from pydantic import BaseModel
from google.adk.tools.tool_context import ToolContext

from toddle_ops.models.enums import Status


class DatabaseAction(BaseModel):
    status: Status
    summary: str
    tool_context: ToolContext
