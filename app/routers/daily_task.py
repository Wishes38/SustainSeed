from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import SessionLocal
from app.schemas import DailyTaskCreate
from app.crud.daily_task import create_and_assign_daily_task

router = APIRouter(prefix="/daily-tasks", tags=["Daily Tasks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


