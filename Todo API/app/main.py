from fastapi import FastAPI

import uvicorn

from api.v1.routers.todo import router
from models.todo import Todo

app = FastAPI(
    title="Todo API",
    description="Simple TODO API with FastAPI + PostgreSQL",
    version="1.0.0"
)

app.include_router(
    router,
    prefix="/api/v1"
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    """Run the FastAPI dev server with auto-reload."""
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )