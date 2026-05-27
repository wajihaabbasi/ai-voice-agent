import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from app.database.connection import Base

class Task(Base):
    __tablename__ = "tasks"

    # Use UUIDs as the primary key for reliable async tracking across state switches
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    
    # Core Task Attributes
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Task Status tracking (pending, processing, completed)
    status = Column(String(50), default="pending", nullable=False)
    
    # for ocntext-awareness - parsed date expressions
    due_at = Column(DateTime(timezone=True), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self) -> dict:
        """Converts database records natively to dictionaries for agent reference."""
        return {
            "id": str(self.id),
            "title": self.title,
            "description": self.description or "",
            "status": self.status,
            "due_at": self.due_at.isoformat() if self.due_at else None,
            "created_at": self.created_at.isoformat()
        }