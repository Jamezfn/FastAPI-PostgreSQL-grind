from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import UserResponse, UserCreate
from app.schemas.token import Token
from app.database import get_db
from app.utils.auth import create_access_token
from app.crud.user import create_user, get_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentification"],
    responses={404: {"description": "Not found"}}
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    new_user = create_user(user=user, db=db)
    if new_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The email is already registered"
        )
    
    return new_user

@router.post("/login", response_model=Token, status_code=status.HTTP_202_ACCEPTED)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Authenticate user and return JWT access token."""
    user = get_user(form_data, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}