from fastapi import HTTPException, status

from app.service.user.base import Base
from app.core.security.hashing import Hash
from app.core.security.token_manager import JWTManager
from app.db.schemas.user.user import UserInCreate, UserResponse, UserLogin, UserWithToken
from app.exceptions import ServiceValidationError

class AuthService(Base):
    def signup(self, user_details: UserInCreate) -> UserResponse:
        """User Create service"""
        if self._userRepository.get_user_by_email(email=user_details.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please login")
        user_details.password = Hash.hash_password(plain_password=user_details.password)

        db_user = self._userRepository.create_user(user_data=user_details.model_dump())
        return UserResponse.model_validate(db_user)
    
    def login(self, loginDetails: UserLogin) -> UserWithToken:
        """User login service"""
        user = self._userRepository.get_user_by_email(email=loginDetails.email)
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please create an account")
        
        if Hash.verify_password(plain_password=loginDetails.password, hash_password=user.password):
            access_token = JWTManager().create_access_token(user_id=user.user_id)
            refresh_token = JWTManager().create_refresh_token(user_id=user.user_id)
            if access_token and refresh_token:
                return UserWithToken(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to process request")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please check your credentials")
    
    def refresh_access_token(self, refresh_token: str) -> dict:
        """Refresh an expired access token using a refresh token"""
        auth_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authentication Credentials"
        )
        
        payload = JWTManager().decode_jwt(token=refresh_token)
        if payload.get("type") != "refresh":
            raise auth_exception
        
        user_id = payload.get("sub")
        if not user_id:
            raise auth_exception
        
        try:
            user = self._userRepository.get_user_by_id(id=user_id)
        except Exception:
            raise auth_exception
        
        _access_token = JWTManager().create_access_token(user_id=user_id)
        _refresh_token = JWTManager().create_refresh_token(user_id=user_id)
        
        if _access_token and _refresh_token:
            return UserWithToken(access_token=_access_token, refresh_token=_refresh_token, token_type="bearer")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to process request")
        