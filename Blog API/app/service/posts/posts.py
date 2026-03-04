from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import TypeAdapter
from fastapi import HTTPException, status

from app.db.models.user import User
from app.db.repository.post.post import PostRepository
from app.db.repository.user.user import UserRepository
from app.db.repository.post.category import CatRepo
from app.db.schemas.posts.post import PostCreate, PostResponse, CursorPostResponse

class PostService:
    def __init__(self, session: Session):
        self._post_repository = PostRepository(session=session)
        self._cat_repository = CatRepo(session=session)
        self._user = UserRepository(session=session)
        self._post_list_adapter = TypeAdapter(List[PostResponse])

    def create_post(self, current_user: User, post_data: PostCreate) -> PostResponse:
        """Create post service"""
        post_dict = post_data.model_dump()
        post_dict["user_id"] = current_user.user_id

        new_post = self._post_repository.create_post(post_dict=post_dict)

        return PostResponse.model_validate(new_post)
    
    def get_posts_by_category(self, category_id: Optional[UUID], user_id: Optional[UUID], cursor: Optional[datetime], limit: int) -> CursorPostResponse:
        """Get post service"""
        if not category_id:
            posts = self._post_repository.get_all_posts(cursor=cursor, limit=limit)
        else:
            category = self._cat_repository.get_category_by_id(category_id=category_id)
            if not category:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
            posts = self._cat_repository.get_posts_by_category(category_id=category_id, cursor=cursor, limit=limit)
        
        return CursorPostResponse(data=self._post_list_adapter.validate_python(posts), next_cursor=posts[-1].created_at if posts else None)
    
    def get_posts_by_author(self, user_id: UUID, cursor: datetime|None, limit: int) -> CursorPostResponse:
        """Get posts by user"""
        if self._user.get_user_by_id(id=user_id):
            posts = self._post_repository.get_posts_by_author(cursor=cursor, user_id=user_id, limit=limit)

            return CursorPostResponse(data=self._post_list_adapter.validate_python(posts), next_cursor=posts[-1].created_at if posts else None)

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    def get_post_by_tag(self, tag_name: str, cursor: Optional[datetime], limit: int = 10) -> CursorPostResponse:
        """Retreive  posts by tag"""
        posts = self._post_repository.get_posts_by_tag(cursor=cursor, tag_name=tag_name, limit=limit)
        return CursorPostResponse(data=self._post_list_adapter.validate_python(posts), next_cursor=posts[-1].created_at if posts else None)