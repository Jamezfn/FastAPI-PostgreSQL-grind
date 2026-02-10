from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base

class Todo(Base):
    """Represents a single todo item in the database."""
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False,
        name="fk_todos_user_id"
    )

    user = relationship("User", back_populates="todos")