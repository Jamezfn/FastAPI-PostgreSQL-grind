from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING
import uuid
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base
from app.db.models.associations import post_categories, post_tags

if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.models.comment import Comment
    from app.db.models.category import Category
    from app.db.models.tag import Tag

class Post(Base):
    __tablename__ = "posts"
    post_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), nullable=False)

    author: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post", cascade="all, delete")
    categories: Mapped[list["Category"]] = relationship(secondary=post_categories, back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(secondary=post_tags, back_populates="posts")