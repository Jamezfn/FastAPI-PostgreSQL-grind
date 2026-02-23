from uuid import UUID
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.db.schemas.user.user import UserResponse, UserInCreate, UserUpdate
from app.core.database import get_db
from app.service.user.user import UserService


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserInCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    return UserService(session=db).create_user(user_details=user_data)

@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: UUID, db: Session = Depends(get_db)):
    """Get User by id"""
    return UserService(session=db).get_user_by_id(user_id )

@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user_by_id(user_id: UUID, user_data: UserUpdate, db: Session = Depends(get_db)):
    """Update user by id"""
    return UserService(session=db).update_user(id=user_id, update_data=user_data)