from sqlalchemy import String
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import TYPE_CHECKING

from app.core.database import Base

if TYPE_CHECKING:
    from app.db.models.post import Post
    from app.db.models.comment import Comment

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="author", cascade="all, delete")
    comments: Mapped[list["Comment"]] = relationship(back_populates="author", cascade="all, delete")