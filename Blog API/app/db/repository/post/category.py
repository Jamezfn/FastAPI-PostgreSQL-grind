from uuid import UUID
from datetime import datetime
from typing import List
from sqlalchemy import desc
from sqlalchemy.orm import selectinload

from ..base import BaseRepository
from app.db.models.post import Post
from app.db.models.category import Category

class CatRepo(BaseRepository):
    def get_category_by_id(self, category_id: UUID):
        """Retrieve category by id"""
        return self.session.query(Category).filter_by(category_id=category_id).first()
        
    def get_posts_by_category(self, category_id: UUID, cursor: datetime | None = None, limit: int = 100) -> List[Post]:
        """Get post by category with cursor pagination"""
        query = self.session.query(Post).join(Post.categories).filter(
            Category.category_id == category_id
        ).options(selectinload(Post.categories))

        if cursor:
            query = query.filter(Post.created_at < cursor)

        return query.order_by(desc(Post.created_at)).limit(limit=limit).all()