from sqlalchemy.orm import Session
from models.todo import Todo
from schemas.todo import TodoCreate, TodoResponse, TodoUpdate

def get_todos(db: Session):
    return db.query(Todo).all()

def get_todo(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()

def create_todo(db: Session, todo: TodoCreate, user_id: int):
    new_todo = Todo(**todo.model_dump(), user_id=user_id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

def update(db: Session, todo_id: int, todo: TodoUpdate):
    db_todo = get_todo(db, todo_id)
    if not db_todo:
        return None
    
    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    db.commit()
    db.refresh(db_todo)

    return db_todo

def delete_todo(db: Session, todo_id: int):
    db_todo = get_todo(db, todo_id)

    if not db_todo:
        return None

    db.delete(db_todo)
    db.commit()

    return db_todo