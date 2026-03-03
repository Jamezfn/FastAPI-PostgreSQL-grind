from app.db.repository.base import BaseRepository
from app.db.models.comment import Comment

class CommentRepository(BaseRepository):
    def create_comment(self, comment_data: dict, ) -> Comment:
        """Create comment for a post"""
        new_comment = Comment(**comment_data)

        self.session.add(new_comment)  
        self.session.flush()

        return new_comment