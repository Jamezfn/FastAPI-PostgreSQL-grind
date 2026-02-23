from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routes import user
from app.core.database import Base, engine

from app.db.models.post import Post
from app.db.models.comment import Comment
from app.db.models.category import Category
from app.db.models.associations import post_categories, post_tags
from app.db.models.tag import Tag

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Database tables created/verified")

    yield

    engine.dispose()
    print("Database connections closed")

app = FastAPI(title="Blog API", lifespan=lifespan)

app.include_router(user.router, prefix="/api/v1")