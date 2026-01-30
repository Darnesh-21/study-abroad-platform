from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User, UserProfile, TodoItem
from app.schemas import TodoCreate, TodoUpdate, TodoResponse
from app.auth_utils import get_current_user
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=List[TodoResponse])
async def get_todos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    include_completed: bool = False
):
    query = db.query(TodoItem).filter(TodoItem.user_id == current_user.id)
    
    if not include_completed:
        query = query.filter(TodoItem.is_completed == False)
    
    todos = query.order_by(TodoItem.created_at.desc()).all()
    return todos

@router.post("/", response_model=TodoResponse)
async def create_todo(
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_todo = TodoItem(
        user_id=current_user.id,
        title=todo_data.title,
        description=todo_data.description,
        priority=todo_data.priority,
        category=todo_data.category,
        due_date=todo_data.due_date,
        ai_generated=False
    )
    
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return new_todo

@router.patch("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todo = db.query(TodoItem).filter(
        TodoItem.id == todo_id,
        TodoItem.user_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    if todo_update.is_completed is not None:
        todo.is_completed = todo_update.is_completed
        if todo_update.is_completed:
            todo.completed_at = datetime.utcnow()
    
    if todo_update.title:
        todo.title = todo_update.title
    if todo_update.description:
        todo.description = todo_update.description
    if todo_update.priority:
        todo.priority = todo_update.priority
    
    db.commit()
    db.refresh(todo)
    
    return todo

@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    todo = db.query(TodoItem).filter(
        TodoItem.id == todo_id,
        TodoItem.user_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    
    return {"message": "Todo deleted successfully"}
