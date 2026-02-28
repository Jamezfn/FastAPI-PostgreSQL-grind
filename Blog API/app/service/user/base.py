from sqlalchemy.orm import Session

from app.db.repository.user.user import UserRepository

class Base:
    def __init__(self, session: Session):
        self._userRepository = UserRepository(session=session)

    @property
    def user_repository(self):
        """Accessor for the user repository"""
        return self._userRepository