from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import TYPE_CHECKING
import uuid
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

if TYPE_CHECKING:
    from app.db.models.post import Post
    from app.db.models.comment import Comment

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="author", cascade="all, delete")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author", cascade="all, delete")