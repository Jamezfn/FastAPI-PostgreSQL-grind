from pydantic import BaseModel, Field, field_validator, ConfigDict
from uuid import UUID
from typing import Optional, List

from app.exceptions import ServiceValidationError

class PostCreate(BaseModel):
    """Schema for creating a new post"""
    title: str = Field(..., min_length=1, max_length=200, description="Post title")
    body: str = Field(..., min_length=1, description="Post content")
    category_ids: Optional[List[UUID]] = Field(default=None, max_length=3, description="List of category IDs to associate with the post")
    tag_ids: Optional[List[UUID]] = Field(default=None, description="List of tag IDs to associate with the post")

    @field_validator('title')
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        """Validate that title is not empty after stripping whitespace"""
        if not v or not v.strip():
            raise ServiceValidationError('Title cannot be empty')
        return v.strip()
    
    @field_validator('body')
    @classmethod
    def body_not_empty(cls, v: str) -> str:
        """Validate that body is not empty after stripping whitespace"""
        if not v or not v.strip():
            raise ServiceValidationError('Body cannot be empty')
        return v.strip()

class CategoryResponse(BaseModel):
    category_id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)

class TagResponse(BaseModel):
    tag_id: UUID
    name: str

    model_config = ConfigDict(from_attributes=True)
    
class PostResponse(BaseModel):
    """Schema for post response after creation"""
    post_id: UUID
    user_id: UUID
    title: str
    body: str
    categories: Optional[List[CategoryResponse]] = None
    tags: Optional[List[TagResponse]] = None

    model_config = ConfigDict(
        from_attributes=True
    )