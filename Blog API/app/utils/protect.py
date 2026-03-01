from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Annotated, Union

from app.db.schemas.user.user import UserResponse
from app.core.security.token_manager import JWTManager
from app.service.user.user import UserService

AUTH_PREFIX = 'Bearer '

def get_current_user(session: Session = Depends(), authorization: Annotated[Union[str, None], Header()] = None) -> UserResponse:
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Authentication Credentials"
    )

    if not authorization:
        raise auth_exception
    
    if not authorization.startswith(AUTH_PREFIX):
        raise auth_exception
    
    payload = JWTManager.decode_jwt(token=authorization[len(AUTH_PREFIX):])
    if payload and payload["user_id"]:
        user = UserService(session=session).get_user_by_id(payload["user_id"])
        return UserResponse.model_validate(user, strict=True)
    raise auth_exception