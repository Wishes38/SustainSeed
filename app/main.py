from fastapi import FastAPI
from app.models import Base
from app.database import engine
from app.routers.auth import router as auth_router
from app.routers.eco_action import router as eco_action_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(eco_action_router)

Base.metadata.create_all(bind=engine)