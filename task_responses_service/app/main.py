from fastapi import FastAPI
from app.database import engine
from app.models.base_schema import Base  # ← импортируем Base отсюда
from app.models.response import ResponseDB
from app.endpoints.responses_router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Responses Service",
    description="Service for managing task responses",
    version="1.0.0"
)

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Task Responses Service is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}