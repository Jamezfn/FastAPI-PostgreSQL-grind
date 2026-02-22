import uuid
from uuid import UUID
from typing import Union, Optional

from ..base import BaseRepository
from app.db.schemas.user.user import UserIncreate, UpdateUser
from app.db.models.user import User

class UserRepository(BaseRepository):
    def create_user(self, user_data: UserIncreate):
        """Create a new user"""
        new_user = User(**user_data.model_dump(exclude_none=True))

        try:
            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)
            return new_user
        except Exception:
            self.session.rollback()
            raise
    
    def user_exist_by_email(self, email: str) -> bool:
        """Check if user exist using email"""
        return self.session.query(User.user_id).filter_by(email=email).first() is not None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve user by email"""
        return self.session.query(User).filter_by(email=email).first()
    
    def get_user_by_id(self, id: Union[str, UUID]) -> Optional[User]:
        """Retrieve user using id"""
        if isinstance(id, str):
            try:
                id = UUID(id)
            except ValueError:
                return None
        
        return self.session.query(User).filter_by(user_id=id).first()
    
    def update_user(self, id: Union[str, UUID], update_data: UpdateUser):
        """Update user by id"""
        user = self.get_user_by_id(id)

        if not user:
            return None
        
        update_dict = update_data.model_dump(exclude_unset=True)

        for key, value in update_dict.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        self.session.commit()
        self.session.refresh(user)

        return user
    
    def delete_user(self, id: Union[str, UUID]) -> bool:
        """Delete user by id"""
        user = self.get_user_by_id(id)
        if not user:
            return False

        try:
            self.session.delete(user)
            self.session.commit()
            return True
        except Exception:
            self.session.rollback()
            raise