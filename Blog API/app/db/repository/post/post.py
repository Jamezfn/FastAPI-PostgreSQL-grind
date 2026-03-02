from ..base import BaseRepository
from app.db.models.post import Post

class PostRepository(BaseRepository):
    def create_post(self, post_data) -> Post:
        """Create a new post"""
        pass