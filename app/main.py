from fastapi import FastAPI
from app.models import Base
from app.database import engine
from app.routers.user import router as user_router

app = FastAPI()


@app.get("/")
async def hello_world():
    return {"message": "Hello World"}

app.include_router(user_router)

Base.metadata.create_all(bind=engine)