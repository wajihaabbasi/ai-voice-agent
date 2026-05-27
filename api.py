import enum
from typing import Annotated, Optional
from livekit.agents import llm
import logging

logger= logging.getLogger("task")
logger.setLevel(logging.INFO) # used to print the output of the agent to the console

class Task:
    class Task:
        def __init__(self, task_id: int, title: str, time: str):
            self.id = task_id
            self.title = title
            self.time = time

    def __str__(self):
        return f"[{self.id}] {self.title} at {self.time}"
    
class TaskState:
    def __init__(self):
        self.tasks = []
        self.next_id = 1


class TaskAssistantFnc(llm.FunctionContext):
    def __init__(self) -> None:
        super().__init__()
        self.state = TaskState()    