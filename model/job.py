from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from model.message import SubjectEnum

from ._agent import AgentEnum, BaseAgent
from .world import World

if TYPE_CHECKING:
    from model.message import Message


class JobStatesEnum(str, Enum):
    AVAILABLE = "available"
    SELECTED = "selected"
    COMPLETE = "complete"


class Job(BaseAgent):
    _status: JobStatesEnum
    _print_time: int
    _submitted_at: int
    _selected_at: int
    _manufactured_by: int
    _completed_at: int

    def __init__(
        self,
        id: int,
        print_time: int,
        world: World,
        debug: bool = False,
    ):
        self._print_time = print_time
        self._submitted_at = world.now()
        self._status = JobStatesEnum.AVAILABLE
        super().__init__(id=id, type=AgentEnum.JOB, world=world, debug=debug)

    def next(self):
        print(f"[JOB {self._id}] Next ({self._status})")
        return

    def receive_message(self, msg: Message):
        print(f"[JOB {self._id}] (Message Received)")
        match msg["subject"]:
            case SubjectEnum.AVAILABILITY_CHECK:
                # Only replies if available
                if self._status == JobStatesEnum.AVAILABLE:
                    reply: Message = {
                        "from_agent": self._id,
                        "to_agents": [msg["from_agent"]],
                        "subject": SubjectEnum.AVAILABLE,
                        "data": {"print_time": self._print_time},
                    }
                    self._world.add_message(reply)
            case SubjectEnum.SELECTED:
                if self._status == JobStatesEnum.AVAILABLE:
                    reply: Message = {
                        "from_agent": self._id,
                        "to_agents": [msg["from_agent"]],
                        "subject": SubjectEnum.ACCEPTED,
                        "data": {"print_time": self._print_time},
                    }
                    self._world.add_message(reply)
                    self._selected_at = self._world.now()
                    self._status = JobStatesEnum.SELECTED
                else:
                    reply: Message = {
                        "from_agent": self._id,
                        "to_agents": [msg["from_agent"]],
                        "subject": SubjectEnum.DECLINED,
                        "data": {},
                    }
                    self._world.add_message(reply)
            case SubjectEnum.COMPLETED:
                self._completed_at = msg["data"]["completed_at"]
                self._status = JobStatesEnum.COMPLETE
            case _:
                exit(
                    f"[JOB {self._id}] Should not receive this message: {msg['subject']}"
                )
        return
