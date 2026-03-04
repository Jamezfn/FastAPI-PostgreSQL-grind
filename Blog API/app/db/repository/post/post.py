from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from typing import Optional, List
from datetime import datetime
from sqlalchemy import desc

from ..base import BaseRepository
from app.db.models.post import Post
from app.db.models.category import Category
from app.db.models.tag import Tag

class PostRepository(BaseRepository):
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
                normalised = list({name.strip().lower() for name in tag_names})

                stmt = insert(Tag).values(
                    [{"name": name} for name in normalised]
                ).on_conflict_do_nothing(index_elements=["name"])
                self.session.execute(stmt)

                all_tags = self.session.query(Tag).filter(Tag.name.in_(normalised)).all()
                new_post.tags.extend(all_tags)

            self.session.commit()
            self.session.refresh(new_post)

            return new_post 

        except Exception:
            self.session.rollback()
            raise

    def get_all_posts(self, cursor: Optional[datetime] = None, limit: int = 100) -> List[Post]:
        """Retrieve all post with pagination"""
        query = self.session.query(Post)
        if cursor:
            query = query.filter(Post.created_at < cursor)
        return query.order_by(desc(Post.created_at)).limit(limit=limit).all()