from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from database import get_db
from models import CategoryModel

router = APIRouter(prefix="/categories", tags=["Categories"])

# Схема для создания категории
class CategoryCreate(BaseModel):
    name: str

@router.get("/")
async def get_categories(db: Session = Depends(get_db)):
    return db.query(CategoryModel).all()

@router.post("/")
async def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    # Проверяем, нет ли уже такой категории
    existing = db.query(CategoryModel).filter(CategoryModel.name == category_data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
        
    new_category = CategoryModel(name=category_data.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

