from fastapi import FastAPI
from app.models import Base
from app.database import engine
from app.routers.user import router as user_router
from app.routers.auth import router as auth_router

app = FastAPI()

@app.get("/")
async def hello_world():
    return {"message": "Hello World"}

app.include_router(user_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)