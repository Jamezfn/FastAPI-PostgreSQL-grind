from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.db.schemas.user.user import UserResponse, UserInCreate
from app.core.database import get_db
from app.service.user.user import UserService
from app.db.schemas.posts.post import PostCreate, PostResponse
from app.utils.protect import get_current_user
from app.db.models.user import User
from app.service.posts.posts import PostService

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(post_data: PostCreate, session: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create post endpoint"""
    return PostService(session=session).create_post(current_user=current_user, post_data=post_data)