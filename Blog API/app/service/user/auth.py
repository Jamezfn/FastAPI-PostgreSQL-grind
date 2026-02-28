from fastapi import HTTPException, status

from app.service.user.base import Base
from app.core.security.hashing import Hash
from app.db.schemas.user.user import UserInCreate, UserResponse, UserUpdate, UserDeleteResponse

class AuthService(Base):
    def signup(self, user_details: UserInCreate) -> UserResponse:
        """User Create service"""
        if self._userRepository.get_user_by_email(email=user_details.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please login")
        user_details.password = Hash.hash_password(plain_password=user_details.password)

        db_user = self._userRepository.create_user(user_data=user_details.model_dump())
        return UserResponse.model_validate(db_user)