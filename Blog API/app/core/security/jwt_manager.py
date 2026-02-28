import jwt
import time
from uuid import UUID

from app.config import settings

class JWTManager:
    """Authentication service for JWT token management"""
    def __init__(self):
        self.jwt_secret = settings.jwt_secret
        self.jwt_algorithmn = settings.jwt_algorithmn

    def sign_jwt(self, user_id: UUID) -> str:
        """Generate JWT token for authenticated user"""
        payload = {
            "user_id": user_id,
            "expire": time.time() + 900
        }

        return jwt.encode(payload, self.jwt_secret, algorithmn=self.jwt_algorithm)
    
    def decode_jwt(self, token: str) -> dict:
        """Verify and decode JWT token"""
        try:
            decode_token = jwt.decode(token, self.jwt_secret, self.jwt_algorithmn)
            return decode_token if decode_token["expire"] >= time.time() else None
        except:
            print("unable to decode token")
            return None