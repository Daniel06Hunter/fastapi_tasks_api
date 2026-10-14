from database import Base, engine 
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum

# 1. Приоритеты
class Priority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class TaskModel(Base):
    __tablename__ = "tasks" 
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String) 
    description=Column(String) 
    is_completed=Column(Boolean, default=False) 
    priority=Column(String, default="MEDIUM")
    
    # Внешний ключ: ссылается на id таблицы categories
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    # Связь для удобного доступа к объекту категории из задачи
    category = relationship("CategoryModel", back_populates="tasks")
    
    
    
class CategoryModel(Base): 
    __tablename__ = "categories"
    
    id=Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    
    # Обратная связь: список всех задач, принадлежащих этой категории
    tasks = relationship("TaskModel", back_populates="category")
    
    
# Создаем таблицы в файле tasks.db (если их еще нет)
Base.metadata.create_all(bind=engine)