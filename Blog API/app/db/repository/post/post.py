from psycopg2 import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from typing import Optional, List, Any, Dict
from datetime import datetime
from sqlalchemy import desc
from uuid import UUID

from ..base import BaseRepository
from app.db.models.post import Post
from app.db.models.category import Category
from app.db.models.tag import Tag

class PostRepository(BaseRepository):
    def _upsert_and_get_tags(self, tag_names: List[str]) -> List[Tag]:
        """
        Bulk insert tags using PostgreSQL ON CONFLICT DO NOTHING
        and fetch all matching tags in a single query.
        """
        if not tag_names:
            return []
        
        normalised = list({name.strip().lower() for name in tag_names})
        stmt = insert(Tag).values([{"name": name} for name in normalised])
        stmt = stmt.on_conflict_do_nothing(index_elements=["name"])
        self.session.execute(stmt)

        return self.session.query(Tag).filter(Tag.name.in_(normalised)).all()

    def create_post(self, post_dict: dict) -> Post:
        """Create a new post"""
        category_ids = post_dict.pop("category_ids", [])
        tag_names = post_dict.pop("tags", [])

        new_post = Post(**post_dict)
        try:
            self.session.add(new_post)
            self.session.flush()

            if category_ids:
                categories = self.session.query(Category).filter(Category.category_id.in_(category_ids)).all()
                new_post.categories.extend(categories)

            if tag_names:
                all_tags = self._upsert_and_get_tags(tag_names)
                new_post.tags.extend(all_tags)

            self.session.commit()
            self.session.refresh(new_post)

            return new_post 

        except Exception:
            self.session.rollback()
            raise

    def get_post_by_id(self, post_id: UUID) -> Post:
        """Get post by id"""
        return self.session.query(Post).filter(Post.post_id==post_id).first()

    def get_all_posts(self, cursor: Optional[datetime] = None, limit: int = 10) -> List[Post]:
        """Retrieve all post with pagination"""
        query = self.session.query(Post)
        if cursor:
            query = query.filter(Post.created_at<cursor)
        return query.order_by(desc(Post.created_at)).limit(limit=limit).all()
    
    def get_posts_by_author(self, cursor: Optional[datetime], user_id: UUID, limit: int = 10) -> List[Post]:
        """Retrieve post for a particular user"""
        query = self.session.query(Post)
        if cursor:
            query = query.filter(Post.created_at < cursor)
        return query.filter(Post.user_id==user_id).order_by(desc(Post.created_at)).limit(limit=limit).all()
    
    def get_posts_by_tag(self, tag_name: str, cursor: Optional[datetime], limit: int = 10) -> List[Post]:
        """Retrieve posts by tag"""
        query = self.session.query(Post)
        if cursor:
            query = query.filter(Post.created_at < cursor)

        return query.join(Post.tags).filter(Tag.name==tag_name.lower().strip()).limit(limit=limit).all()
    
    def update_post(self, post_id: str, update_data: Dict[str, Any]) -> Optional[Post]:
        """Update post"""
        post = self.get_post_by_id(post_id=post_id)
        if not post:
            return None
        category_ids = update_data.pop("categories_ids", None)
        if category_ids is not None:
            categories = self.session.query(Category).filter(Category.category_id.in_(category_ids)).all()
            post.categories = categories
        
        tag_names = update_data.pop("tags", None)
        if tag_names is not None:
            post.tags = self._upsert_and_get_tags(tag_names)

        for key, value in update_data.items():
            if key in Post.__table__.columns.keys():
                setattr(post, key, value)

        try:
            self.session.commit()
            self.session.refresh(post)

            return post
        
        except IntegrityError:
            self.session.rollback()
            raise
    
    def delete_post(self, post_id: str) -> bool:
        post = self.get_post_by_id(post_id=post_id)
        self.session.delete(post)
        self.session.commit()
        return True