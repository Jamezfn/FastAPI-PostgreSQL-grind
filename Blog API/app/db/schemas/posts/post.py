from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from typing import Optional, List

from app.exceptions import ServiceValidationError

class PostCreate(BaseModel):
    """Schema for creating a new post"""
    title: str = Field(..., min_length=1, max_length=200, description="Post title")
    body: str = Field(..., min_length=1, description="Post content")
    category_ids: Optional[List[UUID]] = Field(default=None, description="List of category IDs to associate with the post")
    tag_ids: Optional[List[UUID]] = Field(default=None, description="List of tag IDs to associate with the post")

    @field_validator
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate that title is not empty after stripping whitespace"""
        if not v or not v.strip():
            raise ServiceValidationError('Title cannot be empty')
    
    @field_validator
    @classmethod
    def body_not_empty(cls, v: str) -> str:
        """Validate that body is not empty after stripping whitespace"""
        if not v or not v.strip():
            raise ServiceValidationError('Body cannot be empty')
        return v.strip()