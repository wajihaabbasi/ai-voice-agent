import logging
from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import TaskModel

logger = logging.getLogger("voice_crud.controller")

class TaskController:
    """
    Handles core business logic interactions for Task records in PostgreSQL.
    All operations are asynchronous to prevent blocking the real-time audio threads.
    """

    @staticmethod
    async def create_task(db: AsyncSession, title: str, time_info: Optional[str] = None) -> TaskModel:
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty.")
        
        task = TaskModel(title=title.strip(), time_info=time_info.strip() if time_info else None)
        db.add(task)
        await db.flush() # Force-generate the auto-increment ID before returning
        return task

    @staticmethod
    async def get_all_tasks(db: AsyncSession) -> List[TaskModel]:
        query = select(TaskModel).order_by(TaskModel.id.asc())
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def update_task(db: AsyncSession, task_id: int, new_title: Optional[str] = None, new_time: Optional[str] = None) -> Optional[TaskModel]:
        query = select(TaskModel).where(TaskModel.id == task_id)
        result = await db.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            return None
        
        if new_title is not None:
            task.title = new_title.strip()
        if new_time is not None:
            task.time_info = new_time.strip()
            
        await db.flush()
        return task

    @staticmethod
    async def delete_task(db: AsyncSession, task_id: int) -> bool:
        query = select(TaskModel).where(TaskModel.id == task_id)
        result = await db.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            return False
            
        await db.delete(task)
        await db.flush()
        return True