from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import SessionLocal
from app.schemas import DailyTaskCreate, DailyTaskOut, DailyTaskUpdate
from app.crud import daily_task as crud
from app.crud.daily_task_ops import clear_all_daily_tasks, assign_daily_tasks_to_all_users

router = APIRouter(prefix="/daily-tasks", tags=["Daily Tasks"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=DailyTaskOut)
def create_task(task: DailyTaskCreate, db: db_dependency):
    return crud.create_daily_task(db, task)


@router.get("/{task_id}", response_model=DailyTaskOut)
def get_task(task_id: int, db: db_dependency):
    task = crud.get_daily_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/", response_model=list[DailyTaskOut])
def get_tasks(db: db_dependency, skip: int = 0, limit: int = 100):
    return crud.get_all_daily_tasks(db, skip, limit)


@router.put("/{task_id}", response_model=DailyTaskOut)
def update_task(task_id: int, task_update: DailyTaskUpdate, db: db_dependency):
    task = crud.update_daily_task(db, task_id, task_update)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}", response_model=DailyTaskOut)
def delete_task(task_id: int, db: db_dependency):
    task = crud.delete_daily_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/assign-daily-tasks")
def assign_tasks(db: db_dependency):
    assign_daily_tasks_to_all_users(db)
    return {"message": "Tasks were assigned."}


@router.post("/clear-daily-tasks")
def clear_tasks(db: db_dependency):
    clear_all_daily_tasks(db)
    return {"message": "Tasks were deleted."}
