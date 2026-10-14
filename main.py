from fastapi import FastAPI 
from routers import tasks, categories 
from database import engine, Base 

# Создаем таблицы в БД при старте
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Structured Tasks API with Categories")

# Подключаем роутер задач
app.include_router(tasks.router)
app.include_router(categories.router)


@app.get("/")
async def root():
    return {"message": "Welcome to Structured Task API! Go to /docs"}






    







