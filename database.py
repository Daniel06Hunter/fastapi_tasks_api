from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCEHMY_DATABASE_URL = "sqlite:///./tasks.db" 

engine= create_engine(SQLALCEHMY_DATABASE_URL, connect_args={"check_same_thread": False}) # (check_same_thread=False нужно только для SQLite в FastAPI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine) 

Base = declarative_base()


# Зависимость для получения сессии БД в эндпоинтах
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
#database.py — только подключение к SQLite и создание сессии