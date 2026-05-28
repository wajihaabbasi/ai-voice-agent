# app/agents/tools.py
from typing import Optional
import logging
from livekit.agents.llm import function_tool
from app.controllers.task_controller import TaskController
from app.database.connection import AsyncSessionLocal

logger = logging.getLogger("task_agent")

class TaskAssistantTools:
    @function_tool
    async def create_task(self, title: str, time_info: Optional[str] = None) -> str:
        """
        Create a new task with a specified title and optional descriptive timing.
        """
        full_title = f"{title} at {time_info}" if time_info else title  

        async with AsyncSessionLocal() as db:
            try:
                task = await TaskController.create_task(db, full_title)
                await db.commit()  # FIXED: Critical to prevent automatic transactional rollback
                return f"Task '{task.title}' successfully created."
            except Exception as e:
                logger.error(f"Error creating task: {e}")
                return f"Failed to save task: {str(e)}"
            
    @function_tool
    async def list_tasks(self) -> str:
        """
        List or read out all current active tasks on the user's agenda.
        """
        async with AsyncSessionLocal() as db:
            tasks = await TaskController.get_all_tasks(db)
            if not tasks:
                return "Your agenda is completely clear. You have no tasks right now."
        
            agenda = []  
            for idx, task in enumerate(tasks, start=1):
                agenda.append(f"Task {idx}: {task.title} [{task.status}]")
            return "Here are your current tasks: " + ", ".join(agenda)   

    @function_tool
    async def update_task(self, search_term: str, new_title: Optional[str] = None, status: Optional[str] = None) -> str:
        """
        Update an existing task matching context lookups like 'the workout' or 'the first task'.
        """
        async with AsyncSessionLocal() as db:
            task = await TaskController.find_task_by_context(db, search_term)
            if not task:
                return f"I couldn't find any task matching '{search_term}'."
        
            # FIXED: Aligned keyword arguments with the controller signatures
            await TaskController.update_task(db, task_id=task.id, new_title=new_title, new_status=status)
            await db.commit()
            return f"Successfully updated task matching '{search_term}'." 
        
    @function_tool
    async def delete_task(self, search_term: str) -> str:
        """
        Permanently delete a task using conversational lookups like 'the first one' or a title keyword.
        """
        async with AsyncSessionLocal() as db:
            task = await TaskController.find_task_by_context(db, search_term)
            if not task:
                return f"I couldn't locate a task matching '{search_term}' to delete."
                
            success = await TaskController.delete_task(db, task_id=task.id)
            if success:
                await db.commit()
                return f"Task '{task.title}' has been successfully deleted."
            return f"Failed to delete the task matching '{search_term}'."'''
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
'''