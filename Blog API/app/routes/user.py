from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.db.schemas.user.user import UserResponse, UserInCreate
from app.core.database import get_db
from app.service.user.user import UserService


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserInCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    service = UserService(session=db)
    return service.create_user(user_details=user_data)