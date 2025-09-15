from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from model.message import SubjectEnum

from ._agent import AgentEnum, BaseAgent
from .world import World

if TYPE_CHECKING:
    from model.message import Message

    pass


class MachineStateEnum(str, Enum):
    AVAILABLE = "available"
    WAITING_FOR_REPLIES = "waiting_for_replies"
    WAITING_FOR_ACCEPTANCE = "waiting_for_acceptance"
    PRINTING = "printing"


class Machine(BaseAgent):
    _status: MachineStateEnum
    _jobs: list[int]
    _timer: int
    _replies: list[int]

    def __init__(
        self,
        id: int,
        world: World,
        debug: bool = False,
    ):
        self._submitted_at = world.now()
        self._status = MachineStateEnum.AVAILABLE
        self._timer = 0
        self._replies = []
        self._jobs = []
        super().__init__(id=id, type=AgentEnum.MACHINE, world=world, debug=debug)

    def next(self):
        print(f"[MACHINE {self._id}] Next ({self._status})")
        match self._status:
            case MachineStateEnum.AVAILABLE:
                self._replies = []
                self._timer = 0
                jobs_ids = self._world.ids(AgentEnum.JOB)
                msg: Message = {
                    "from_agent": self._id,
                    "to_agents": jobs_ids,
                    "subject": SubjectEnum.AVAILABILITY_CHECK,
                    "data": {},
                }
                self._world.add_message(msg)
                self._timer = 4
                self._status = MachineStateEnum.WAITING_FOR_REPLIES
            case MachineStateEnum.WAITING_FOR_REPLIES:
                if self._timer == 0:
                    if len(self._replies) > 0:
                        job = self._replies[0]
                        msg: Message = {
                            "from_agent": self._id,
                            "to_agents": [job],
                            "subject": SubjectEnum.SELECTED,
                            "data": {},
                        }
                        self._world.add_message(msg)
                        self._status = MachineStateEnum.WAITING_FOR_ACCEPTANCE
                    else:
                        self._replies = []
                        self._timer = 0
                        self._status = MachineStateEnum.AVAILABLE
                else:
                    self._timer -= 1
                pass
            case MachineStateEnum.WAITING_FOR_ACCEPTANCE:
                pass
            case MachineStateEnum.PRINTING:
                if self._timer == 0:
                    msg: Message = {
                        "from_agent": self._id,
                        "to_agents": [self._jobs[-1]],
                        "subject": SubjectEnum.COMPLETED,
                        "data": {"completed_at": self._world.now()},
                    }
                    self._world.add_message(msg)
                    self._status = MachineStateEnum.AVAILABLE
                    self._replies = []
                    self._timer = 0
                else:
                    self._timer -= 1

    def receive_message(self, msg: Message):
        print(f"[MACHINE {self._id}] Received ({msg['subject']})")
        match (msg["subject"], self._status):
            case (SubjectEnum.AVAILABLE, MachineStateEnum.WAITING_FOR_REPLIES):
                self._replies.append(msg["from_agent"])
            case (SubjectEnum.ACCEPTED, MachineStateEnum.WAITING_FOR_ACCEPTANCE):
                self._timer = msg["data"]["print_time"]
                self._status = MachineStateEnum.PRINTING
                self._jobs.append(msg["from_agent"])
            case (SubjectEnum.DECLINED, MachineStateEnum.WAITING_FOR_ACCEPTANCE):
                self._timer = 0
                self._replies = []
                self._status = MachineStateEnum.AVAILABLE
            case _:
                pass
        return
