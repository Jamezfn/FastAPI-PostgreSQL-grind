from sqlalchemy import Table, Column, ForeignKey

from app.core.database import Base

post_categories = Table(
    "post_categories",
    Base.metadata,
    Column("post_id", ForeignKey("posts.post_id", ondelete="CASCADE"), primary_key=True),
    Column("category_id", ForeignKey("categories.category_id", ondelete="CASCADE"), primary_key=True)
)

post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("posts.post_id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.tag_id", ondelete="CASCADE"), primary_key=True)
)