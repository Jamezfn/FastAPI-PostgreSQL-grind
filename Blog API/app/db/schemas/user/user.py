from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from uuid import UUID

class UserInCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    password: str

    model_config = ConfigDict(from_attributes=True)

class UserDeleteResponse(BaseModel):
    message: str
    user_id: UUID