from sqlalchemy.orm import Session

from app.db.models.user import User
from app.db.repository.post.post import PostRepository
from app.db.schemas.posts.post import PostCreate, PostResponse

class PostService:
    def __init__(self, session: Session):
        self._post_repository = PostRepository(session=session)

    def create_post(self, current_user: User, post_data: PostCreate) -> PostResponse:
        """Create post service"""
        post_dict = post_data.model_dump()
        post_dict["user_id"] = current_user.user_id

        new_post = self._post_repository.create_post(post_dict=post_dict)

        return PostResponse.model_validate(new_post)