from uuid import UUID
from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from app.db.schemas.user.user import UserResponse, UserInCreate, UserWithToken, UserLogin, TokenRefresh
from app.core.database import get_db
from app.service.user.user import UserService
from app.service.user.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def sign_up(user_data: UserInCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    return AuthService(session=db).signup(user_details=user_data)

@router.post("/login", response_model=UserWithToken, status_code=status.HTTP_200_OK)
def login(loginDetails: UserLogin, session: Session = Depends(get_db)) -> UserWithToken:
    return AuthService(session=session).login(loginDetails=loginDetails)

@router.post("/refresh", response_model=UserWithToken, status_code=status.HTTP_200_OK)
async def refresh_token(token_data: TokenRefresh, session: Session = Depends(get_db)
):
    """Refresh an expired access token using a refresh token."""
    return AuthService(session=session).refresh_access_token(refresh_token=token_data.refresh_token)