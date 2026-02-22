from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
import uuid
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base
from app.db.models.associations import post_categories

if TYPE_CHECKING:
    from app.db.models.post import Post

class Category(Base):
    __tablename__ = "categories"
    category_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(secondary=post_categories, back_populates="categories")