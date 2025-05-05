from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import *
from app.core.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from app.crud import daily_task as crud

router = APIRouter(prefix="/daily-tasks", tags=["Daily Tasks"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=DailyTaskRead)
def create_task(task_data: DailyTaskCreate, db: Session = Depends(get_db)):
    return crud.create_daily_task(db, task_data)


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    crud.delete_daily_task(db, task_id)
    return {"detail": "Task deleted"}


@router.get("/", response_model=list[DailyTaskRead])
def list_tasks(db: Session = Depends(get_db)):
    return crud.get_all_daily_tasks(db)


@router.post("/assign")
def assign_to_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_data = decode_access_token(token)
    if not user_data or "id" not in user_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    crud.assign_tasks_to_user(db, user_id=user_data["id"])
    return {"detail": "Tasks assigned"}


@router.get("/my-assignments", response_model=list[AssignmentRead])
def my_assignments(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_data = decode_access_token(token)
    if not user_data or "id" not in user_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return crud.get_user_assignments(db, user_id=user_data["id"])


@router.post("/complete/{assignment_id}", response_model=AssignmentRead)
def complete_assignment(assignment_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_data = decode_access_token(token)
    if not user_data or "id" not in user_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    result = crud.complete_task(db, assignment_id, user_id=user_data["id"])
    if not result:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return result
