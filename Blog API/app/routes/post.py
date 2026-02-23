from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.db.schemas.user.user import UserResponse, UserInCreate
from app.core.database import get_db
from app.service.user.user import UserService


router = APIRouter(prefix="/posts", tags=["posts"])

# @rou