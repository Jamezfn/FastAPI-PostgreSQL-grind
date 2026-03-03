from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.utils.protect import get_current_user
from app.db.models.user import User
from app.service.comment.comment import CommentService
from app.db.schemas.comment.comment import CommentCreate, CommentResponse

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/posts/{post_id}/comments", response_model=CommentResponse)
def create_comment(post_id: UUID, comment_data: CommentCreate, session: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """Create comment route"""
    return CommentService(session=session).create_comment(comment_data=comment_data, post_id=post_id, current_user=user)