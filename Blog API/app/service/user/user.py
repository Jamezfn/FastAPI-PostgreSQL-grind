from uuid import UUID
from typing import Union, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

from app.db.repository.user.user import UserRepository
from app.db.schemas.user.user import UserInCreate, UserResponse, UserUpdate, UserDeleteResponse
from app.core.security.hashing import Hash

class UserService:
    def __init__(self, session: Session):
        self.__userRepository = UserRepository(session=session)

    def create_user(self, user_details: UserInCreate) -> UserResponse:
        """User Create service"""
        if self.__userRepository.get_user_by_email(email=user_details.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please login")
        user_details.password = Hash.hash_password(plain_password=user_details.password)

        db_user = self.__userRepository.create_user(user_data=user_details)
        return UserResponse.model_validate(db_user)
    
    def get_user_by_id(self, id: Union[str, UUID]) -> UserResponse:
        """Retrieve user by id service"""
        user = self.__userRepository.get_user_by_id(id=id)
        if user:
            return UserResponse.model_validate(user)
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    def update_user(self, id: Union[str, UUID], update_data: UserUpdate) -> UserResponse:
        """Update user service"""
        existing_user = self.__userRepository.get_user_by_id(id)
        if not existing_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        if update_data.email and update_data.email != existing_user.email:
            if self.__userRepository.get_user_by_email(email=update_data.email):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
            
        try:
            update_dict = update_data.model_dump(exclude_unset=True)
            updated_user = self.__userRepository.update_user(id=id, update_data=update_dict)

            return UserResponse.model_validate(updated_user)
        except IntegrityError as e:
            if hasattr(e, 'args') and len(e.args) > 1 and isinstance(e.args[1], dict):
                error_info = e.args[1]
                if error_info.get('field') == 'username':
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists.")
                elif error_info.get('field') == 'email':
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists.")
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Update failed due to duplicate data.")
    
    def delete_user(self, id: Union[str, UUID]) -> dict:
        """Delete user service - with business logic validation"""
        user = self.__userRepository.get_user_by_id(id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        deleted = self.__userRepository.delete_user(id=id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete user")
        
        return UserDeleteResponse(
            message="User successfully deleted",
            user_id=UUID(str(id)) if isinstance(id, str) else id
        )
        
