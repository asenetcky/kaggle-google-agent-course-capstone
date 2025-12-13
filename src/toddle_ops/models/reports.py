from pydantic import BaseModel

from toddle_ops.enums import Status


# # TODO add description annotations etc...
class StatusReport(BaseModel):
    status: Status
    message: str | None


# class SafetyReport(BaseModel):
#     """A safety report for a project."""

#     status: SafetyStatus = Field(..., description="The safety status of the project.")
#     suggestions: List[str] = Field(
#         default_factory=list,
#         description="Suggestions for improving safety if revision is needed.",
#     )
#     summary: str = Field(..., description="A concise summary of the safety assessment.")
