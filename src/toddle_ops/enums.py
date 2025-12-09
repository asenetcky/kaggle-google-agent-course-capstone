from enum import Enum


class Status(str, Enum):
    """Status for common checks and loops."""

    APPROVED = "approved"
    PENDING = "pending"
    REVISION_NEEDED = "revision_needed"
    REJECTED = "rejected"
