# app/crud/daily_task_ops.py

from sqlalchemy.orm import Session
from app.models import User, DailyTask, UserTaskLog

def assign_daily_tasks_to_user(db: Session, user_id: int):
    active_tasks = db.query(DailyTask).filter(DailyTask.active == True).all()
    for task in active_tasks:
        db.add(UserTaskLog(user_id=user_id, daily_task_id=task.id, completed=False))
    db.commit()

def assign_daily_tasks_to_all_users(db: Session):
    for user in db.query(User).all():
        assign_daily_tasks_to_user(db, user.id)

def clear_all_daily_tasks(db: Session):
    db.query(UserTaskLog).filter(UserTaskLog.daily_task_id != None).delete()
    db.commit()
