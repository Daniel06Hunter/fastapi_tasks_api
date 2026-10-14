from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import TaskModel, CategoryModel
from pydantic import BaseModel
from enum import Enum

# Создаем роутер для задач (префикс /tasks сэкономит нам написание пути)
router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Pydantic схемы (их тоже можно вынести в schemas.py, но пока оставим здесь для наглядности)
class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class TaskCreate(BaseModel):
    title: str
    description: str
    priority: Priority = Priority.MEDIUM
    category_id: int | None = None  # Теперь можем передать ID категории

@router.get("/")
async def get_tasks(db: Session = Depends(get_db)):
    return db.query(TaskModel).all()

@router.post("/")
async def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    new_task = TaskModel(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority.value,
        category_id=task_data.category_id,
        is_completed=False
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@router.patch("/{task_id}/complete")
async def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Not Found")
    
    task.is_completed = True
    db.commit()
    db.refresh(task)
    return {"message": "Task completed!", "task_id": task.id}

@router.delete("/{task_id}")
async def delete_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Not Found")
        
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}