from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import DailyTask, UserDailyTaskAssignment, User
from app.schemas import DailyTaskCreate


def create_daily_task(db: Session, task_data: DailyTaskCreate) -> DailyTask:
    new_task = DailyTask(
        title=task_data.title,
        description=task_data.description,
        xp_earned=7.0  # Sabit XP değeri
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def delete_daily_task(db: Session, task_id: int):
    task = db.query(DailyTask).get(task_id)
    if task:
        db.delete(task)
        db.commit()


def get_all_daily_tasks(db: Session):
    return db.query(DailyTask).all()


def assign_tasks_to_user(db: Session, user_id: int):
    today = datetime.utcnow().date()

    already_assigned = db.query(UserDailyTaskAssignment).filter(
        UserDailyTaskAssignment.user_id == user_id,
        UserDailyTaskAssignment.assigned_at >= today
    ).count()

    if already_assigned == 0:
        tasks = db.query(DailyTask).filter(DailyTask.active == True).all()
        for task in tasks:
            assignment = UserDailyTaskAssignment(
                user_id=user_id,
                daily_task_id=task.id,
                completed=False
            )
            db.add(assignment)
        db.commit()


def get_user_assignments(db: Session, user_id: int):
    return db.query(UserDailyTaskAssignment).filter(UserDailyTaskAssignment.user_id == user_id).all()


def complete_task(db: Session, assignment_id: int, user_id: int):
    assignment = db.query(UserDailyTaskAssignment).filter_by(id=assignment_id, user_id=user_id).first()

    if assignment and not assignment.completed:
        assignment.completed = True

        task = db.query(DailyTask).filter_by(id=assignment.daily_task_id).first()
        if task:
            user = db.query(User).filter_by(id=user_id).first()
            if user:
                user.xp += task.xp_earned
                user.update_plant_stage()

        db.commit()
        db.refresh(assignment)
        return assignment

    return None
