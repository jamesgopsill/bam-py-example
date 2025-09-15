from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from model.message import Message

    from .world import World


class AgentEnum(str, Enum):
    JOB = "job"
    MACHINE = "machine"


class BaseAgent:
    _world: World
    _debug: bool
    _id: int
    _type: AgentEnum
    _messages_sent: int
    _messages_received: int

    def __init__(
        self,
        id: int,
        type: AgentEnum,
        world: World,
        debug: bool = False,
    ) -> None:
        self._world = world
        self._debug = debug
        self._id = id
        self._type = type
        self._messages_sent = 0
        self._messages_received = 0

    def id(self) -> int:
        return self._id

    def type(self) -> AgentEnum:
        return self._type

    def next(self):
        return

    def receive_message(self, msg: Message):
        return
