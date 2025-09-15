from enum import Enum
from typing import TypedDict


class SubjectEnum(str, Enum):
    AVAILABLE = "available"
    AVAILABILITY_CHECK = "availability_check"
    SELECTED = "selected"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    COMPLETED = "completed"


class Message(TypedDict):
    from_agent: int
    to_agents: list[int]
    subject: SubjectEnum
    data: dict[str, int]
