from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.todo import TodoResponse, TodoCreate, TodoUpdate
from schemas.user import UserResponse
from crud.crud import create_todo, get_todo ,get_todos, update, delete_todo
from database import get_db
from app.utils.dependencies import get_current_user

router = APIRouter(
    prefix="/todos",
    tags=["Todos"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_new_todo(todo: TodoCreate, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return create_todo(db, todo, current_user.id)

@router.get("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def read_todo(todo_id: int, db: Session=Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return get_todo(db, todo_id)

@router.get("/", response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
def  read_todos(db: Session=Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return get_todos(db)

@router.put("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session=Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    updated = update(db, todo_id, todo)

    if not updated:
            raise HTTPException(status_code=404, detail="Todo not found")
    
    return updated

@router.delete("/todos/{todo_id}")
def deleting_todo(todo_id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    deleted = delete_todo(db, todo_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"message": "Todo deleted successfully"}
