from fastapi import HTTPException, status

from app.service.user.base import Base
from app.core.security.hashing import Hash
from app.core.security.token_manager import JWTManager
from app.db.schemas.user.user import UserInCreate, UserResponse, UserLogin, UserWithToken

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
        if not self._userRepository.user_exist_by_email(email=loginDetails.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please create an account")
        
        user = self._userRepository.get_user_by_email(email=loginDetails.email)
        if Hash.verify_password(plain_password=loginDetails.password, hash_password=user.password):
            token = JWTManager().sign_jwt(user_id=user.user_id)
            if token:
                return UserWithToken(token=token)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unable to process request")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please check your credentials")