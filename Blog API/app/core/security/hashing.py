from bcrypt import checkpw, hashpw, gensalt

class Hash():
    @staticmethod
    def verify_password(plain_password: str, hash_password: bytes) -> bool:
        """Verify a plain password against a bcrypt hash."""
        return checkpw(password=plain_password.encode('utf-8'), hashed_password=hash_password)
    
    @staticmethod
    def hash_password(plain_password: str) -> bytes:
        """Generate a bcrypt hash for a plain password."""
        return hashpw(password=plain_password.encode('utf-8'), salt=gensalt())