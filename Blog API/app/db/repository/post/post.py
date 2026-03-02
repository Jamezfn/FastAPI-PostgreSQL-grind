from sqlalchemy.orm import Session

from ..base import BaseRepository
from app.db.models.post import Post
from app.db.models.category import Category
from app.db.models.tag import Tag

class PostRepository(BaseRepository):
    def create_post(self, post_dict: dict) -> Post:
        """Create a new post"""
        category_ids = post_dict.pop("category_ids", [])
        tag_ids = post_dict.pop("tag_ids", [])

        new_post = Post(**post_dict)
        try:
            self.session.add(new_post)
            self.session.flush()

            if category_ids:
                categories = self.session.query(Category).filter(Category.category_id.in_(category_ids)).all()
                new_post.categories.extend(categories)

            if tag_ids:
                tags = self.session.query(Tag).filter(Tag.tag_id.in_(tag_ids)).all()
                new_post.tags.extend(tags)

            self.session.commit()
            self.session.refresh(new_post)

            return new_post 

        except Exception:
            self.session.rollback()
            raise