from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routes import user
from app.core.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Database tables created/verified")

    yield

    engine.dispose()
    print("Database connections closed")

app = FastAPI(title="Blog API", lifespan=lifespan)

app.include_router(user.router, prefix="/api/v1")