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

#tasks CRUD operations:
# create a task
    @llm.ai_callable(description="Create a new task with title and time")
    def create_task(
        self,
        title: Annotated[str, llm.TypeInfo(description="Task description")],
        time: Annotated[str, llm.TypeInfo(description="Task time (e.g. 10 AM)")],
    ):
        task = Task(self.state.next_id, title, time)
        self.state.tasks.append(task)
        self.state.next_id += 1

        logger.info(f"Created task: {task}")
        return f"Task created: {task}"
    
#read/ list/ fetch tasks
    @llm.ai_callable(description="Get all tasks or agenda")
    def list_tasks(self):
        if not self.state.tasks:
            return "You have no tasks."

        agenda = "\n".join(str(t) for t in self.state.tasks)
        return f"Your tasks are:\n{agenda}"