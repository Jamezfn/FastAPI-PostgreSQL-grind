from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password, verify_password

def create_user(user, db: Session):
    """Create a new user"""
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        return None
    
    hashed_password = hash_password(user.password)
    new_user = User(
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get_user(form_data, db: Session):
    """Get user from the database."""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        return None
    
    return user