from pydantic import BaseModel, Field, ConfigDict, field_validator
from uuid import UUID
from datetime import datetime

from app.exceptions import ServiceValidationError

class CommentCreate(BaseModel):
    body: str = Field(..., min_length=1, max_length=1000)

    @field_validator('body')
    @classmethod
    def body_not_empty(cls, v: str) -> str:
        """Validate that body is not empty after stripping whitespace"""
        if not v or not v.strip():
            raise ServiceValidationError('Body cannot be empty')
        return v.strip()

class CommentAuthor(BaseModel):
    user_id: UUID
    username: str

    model_config = ConfigDict(from_attributes=True)



class CommentResponse(BaseModel):
    comment_id: UUID
    post_id: UUID
    body: str
    created_at: datetime
    author: CommentAuthor

    model_config = ConfigDict(from_attributes=True)