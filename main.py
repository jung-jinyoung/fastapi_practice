from fastapi import FastAPI

from database.db_connection import engine
from database.orm import Base

from routers.todo import router as todos_router
from routers.user import router as users_router

# 테이블 생성 지시
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(todos_router)
app.include_router(users_router)