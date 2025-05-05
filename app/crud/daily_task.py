from sqlalchemy.orm import Session
from app.models import DailyTask
from app.schemas import DailyTaskCreate, DailyTaskUpdate


def create_daily_task(db: Session, task_data: DailyTaskCreate):
    task = DailyTask(**task_data.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_daily_task(db: Session, task_id: int):
    return db.query(DailyTask).filter(DailyTask.id == task_id).first()


def get_all_daily_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DailyTask).offset(skip).limit(limit).all()


def update_daily_task(db: Session, task_id: int, task_data: DailyTaskUpdate):
    task = db.query(DailyTask).filter(DailyTask.id == task_id).first()
    if task:
        for key, value in task_data.dict(exclude_unset=True).items():
            setattr(task, key, value)
        db.commit()
        db.refresh(task)
    return task


def delete_daily_task(db: Session, task_id: int):
    task = db.query(DailyTask).filter(DailyTask.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    return task
