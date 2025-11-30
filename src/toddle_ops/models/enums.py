from enum import Enum


# TODO implement this enum - like with safety etc...
class Status(str, Enum):
    """The difficulty of the project."""

    APPROVED = "approved"
    PENDING = "pending"
    REVISION_NEEDED = "revision needed"
    REJECTED = "rejected"
