from model._agent import AgentEnum, BaseAgent
from model.message import Message


class World:
    _now: int
    _agents: dict[int, BaseAgent]
    _agents_by_type: dict[AgentEnum, list[int]]
    _messages: dict[int, list[Message]]

    def __init__(self) -> None:
        self._now = 0
        self._agents = {}
        self._agents_by_type = {AgentEnum.MACHINE: [], AgentEnum.JOB: []}
        self._messages = {}

    def tick(self) -> None:
        self._now += 1

    def now(self) -> int:
        return self._now

    def reset(self):
        self._now = 0
        self._agents = {}
        self._agents_by_type = {AgentEnum.MACHINE: [], AgentEnum.JOB: []}
        self._messages = {}

    def add_message(self, msg: Message):
        next_step = self.now() + 1
        if next_step in self._messages:
            self._messages[next_step].append(msg)
        else:
            self._messages[next_step] = [msg]

    def send_messages(self):
        now = self.now()
        if now in self._messages:
            for msg in self._messages[now]:
                for id in msg["to_agents"]:
                    if id not in self._agents:
                        exit(f"Agent not in population: Received {id}")
                    else:
                        self._agents[id].receive_message(msg)

    def add_agent(self, agent: BaseAgent):
        if agent.id() in self._agents:
            exit(f"Agent with id already exists. Received: {agent.id}")
        self._agents[agent.id()] = agent
        self._agents_by_type[agent.type()].append(agent.id())

    def call_next(self):
        for _, agent in self._agents.items():
            agent.next()

    def ids(self, type: AgentEnum):
        return self._agents_by_type[type]
