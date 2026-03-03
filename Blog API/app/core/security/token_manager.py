import jwt
import time
from uuid import UUID

from app.config import settings
from app.exceptions import ServiceValidationError

class JWTManager:
    """Authentication service for JWT token management"""
    def __init__(self):
        self.jwt_secret = settings.jwt_secret.get_secret_value()
        self.jwt_algorithmn = settings.jwt_algorithm
        self.access_exp_minutes = 15
        self.refresh_exp_days = 7

    def create_access_token(self, user_id: UUID) -> str:
        """Generate JWT token for authenticated user"""
        payload = {
            "sub": str(user_id),
            "type": "access",
            "exp": int(time.time() + 900)
        }

        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithmn)
    
    def create_refresh_token(self, user_id: UUID) -> str:
        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": int(time.time() + (60 * 60 * 24 * 7)),
        }

        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithmn)
    
    def decode_jwt(self, token: str) -> dict:
        """Verify and decode JWT token"""
        try:
            return jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithmn])
        except jwt.ExpiredSignatureError:
            raise ServiceValidationError('Invalid token')
        except jwt.InvalidTokenError:
            raise ServiceValidationError('Invalid token')