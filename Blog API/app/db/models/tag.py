from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.core.database import Base
from app.db.models.associations import post_tags

if TYPE_CHECKING:
    from app.db.models.post import Post

class Tag(Base):
    __tablename__ = "tags"
    tag_id: Mapped = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(secondary=post_tags, back_populates="tags")