from uuid import UUID
from typing import Union, Optional
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

from ..base import BaseRepository
from app.db.models.user import User

class UserRepository(BaseRepository):
    def create_user(self, user_data: dict) -> User:
        """Create a new user"""
        new_user = User(**user_data)

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
    
    def update_user(self, id: Union[str, UUID], update_data: dict) -> User:
        """Update user by id"""
        user = self.get_user_by_id(id)

        if not user:
            return None
        
        original_username = user.username  

        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        try:
            self.session.commit()
            self.session.refresh(user)

            return user
        
        except IntegrityError as e:
            self.session.rollback()

            if 'username' in update_data:
                user.username = original_username

            if isinstance(e.orig, UniqueViolation):
                if 'username' in str(e.orig):
                    e.args = (*e.args, {"field": "username", "error": "already_exists"})
                elif 'email' in str(e.orig):
                    e.args = (*e.args, {"field": "email", "error": "already_exists"})
            raise

    
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