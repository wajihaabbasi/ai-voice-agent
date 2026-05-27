import enum
from typing import Annotated, Optional
from livekit.agents import llm
import logging
from app.controlles.task_controller import TaskController
from app.database.connection import AsyncSessionLocal

logger= logging.getLogger("task_agent")
logger.setLevel(logging.INFO) # used to print the output of the agent to the console

class TaskAssistnatTools(llm.FunctionContext):
    def __init__(self) -> None:
        super().__init__()
        
    @llm.ai_callable(description="Create a new task with a specified title and optional descriptive timing.")
    async def create_task(
        self,
        title: Annotated[str, llm.TypeInfo(description="The core description or name of the task")],
        time_info: Annotated[Optional[str], llm.TypeInfo(description="Optional time phrasing, e.g., '10 AM' or 'tomorrow morning'")] = None
    ) -> str:
        # Build out a clean compound title if the user specified a time verbally
        full_title = f"{title} ({time_info})" if time_info else title  

        async with AsyncSessionLocal() as db:
            try:
                task = await TaskController.create_task(db, full_title)
                logger.info(f"Created task: {task.title} with ID {task.id}")
                return f"Task {task.title} successfully created"
            except Exception as e:
                logger.error(f"Error creating task: {e}")
                return  f"Failed to save task due to a database exception: {str(e)}"
            
        @llm.ai_callable(description="List or read out all current active tasks on the user's agenda.")
        async def list_tasks(self) -> str:
            async with AsyncSessionLocal() as db:
                tasks = await TaskController.get_all_tasks(db)
                if not tasks:
                    return "Your agenda is completely clear. You have no tasks right now."
            
            # Formulate clean verbal responses avoiding confusing raw IDs
            agenda = []  #list to hold all the created/existing tasks
            for idx, task in enumerate(tasks, start=1):
                agenda.append(f"Task {idx}: {task.title}")
            
            return "Here are your tasks: " + ", ".join(agenda)   

        @llm.ai_callable(description="Update an existing task's title or status matching context lookups like 'the workout' or 'the first task'.")
        async def update_task(
            self,
            search_term: Annotated[str, llm.TypeInfo(description="The verbal identifier or index sequence used to locate the task")],
            new_title: Annotated[Optional[str], llm.TypeInfo(description="The updated title content")] = None,
            status: Annotated[Optional[str], llm.TypeInfo(description="The updated status parameters, like 'completed'")] = None
            ) -> str:
            async with AsyncSessionLocal() as db:
            # Context-Aware lookup matching your fuzzy strategy
                task = await TaskController.find_task_by_context(db, search_term)
                if not task:
                    return f"I couldn't find any task matching '{search_term}' in your records."
            
                await TaskController.update_task(db, task_id=task.id, title=new_title, status=status)
                await db.commit()
                return f"Task updated." 
            
        @llm.ai_callable(description="Delete a specific task permanently by referencing its title name or numerical sequence position.")
        async def delete_task(
        self,
        search_term: Annotated[str, llm.TypeInfo(description="The identifier name or index location spoken by the user")]
    ) -> str:
            async with AsyncSessionLocal() as db:
                task = await TaskController.find_task_by_context(db, search_term)
                if not task:
                    return f"I couldn't find a task matching '{search_term}' to remove."
                
                await TaskController.delete_task(db, task_id=task.id)
                await db.commit()
                return f"Successfully deleted the task: '{task.title}'."   

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
    
#update a task
    @llm.ai_callable(description="Update a task by id with new title and/or time")
    def update_task(
        self,
        task_id: Annotated[int, llm.TypeInfo(description="Task ID")],
        new_title: Annotated[Optional[str], llm.TypeInfo(description="New title")] = None,
        new_time: Annotated[Optional[str], llm.TypeInfo(description="New time")] = None,
    ):
        for task in self.state.tasks:
            if task.id == task_id:
                if new_title:
                    task.title = new_title
                if new_time:
                    task.time = new_time

                logger.info(f"Updated task: {task}")
                return f"Task updated: {task}"

        return "Task not found."  #scenario handling when no task found
    
#delete a task    
    @llm.ai_callable(description="Delete a task by id")
    def delete_task(
        self,
        task_id: Annotated[int, llm.TypeInfo(description="Task ID")],
    ):
        for i, task in enumerate(self.state.tasks):
            if task.id == task_id:
                removed = self.state.tasks.pop(i)
                logger.info(f"Deleted task: {removed}")
                return f"Deleted task: {removed}"

        return "Task not found."  #scenario handling when no task found