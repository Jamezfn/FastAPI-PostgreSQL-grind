from sqlalchemy.orm import Session
from uuid import UUID

from app.db.repository.comment.comment import CommentRepository
from app.db.schemas.comment.comment import CommentCreate, CommentResponse
from app.db.models.user import User

class CommentService:
    def __init__(self, session: Session):
        self._comment_repository = CommentRepository(session=session)

    def create_comment(self, comment_data: CommentCreate, post_id: UUID, current_user: User) -> CommentResponse:
        """Create user handler"""
        comment_dict = comment_data.model_dump()
        comment_dict["post_id"] = post_id
        comment_dict["user_id"] = current_user.user_id

        with self.session.begin():
            comment = self._comment_repository.create_comment(comment_data=comment_dict)
            
        return CommentResponse.model_validate(comment)