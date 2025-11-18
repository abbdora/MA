from fastapi import FastAPI
from .database import engine
from .schemas.base_schema import Base
from .endpoints.auth_router import auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Auth Service')

app.include_router(auth_router, prefix='/api')

@app.get('/')
def read_root():
    return {'message': 'Auth Service with PostgreSQL is running!'}