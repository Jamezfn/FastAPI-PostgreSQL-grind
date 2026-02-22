from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserIncreate(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

class UpdateUser(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)