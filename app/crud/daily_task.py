from sqlalchemy.orm import Session
from datetime import datetime, UTC
from app.models import DailyTask, UserDailyTaskAssignment, User
from app.schemas import DailyTaskCreate
from sqlalchemy import cast, Date


def create_daily_task(db: Session, task_data: DailyTaskCreate) -> DailyTask:
    new_task = DailyTask(
        title=task_data.title,
        description=task_data.description,
        xp_earned=7.0
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def delete_daily_task(db: Session, task_id: int):
    task = db.get(DailyTask, task_id)
    if task:
        db.delete(task)
        db.commit()


def get_all_daily_tasks(db: Session):
    return db.query(DailyTask).all()


def assign_tasks_to_user(db: Session, user_id: int):
    today = datetime.now(UTC).date()
    now = datetime.now(UTC)

    try:
        tasks = db.query(DailyTask).filter(DailyTask.active == True).all()
        for task in tasks:
            already_assigned = db.query(UserDailyTaskAssignment).filter(
                UserDailyTaskAssignment.user_id == user_id,
                UserDailyTaskAssignment.daily_task_id == task.id,
                cast(UserDailyTaskAssignment.assigned_at, Date) == today
            ).first()

            if not already_assigned:
                assignment = UserDailyTaskAssignment(
                    user_id=user_id,
                    daily_task_id=task.id,
                    completed=False,
                    assigned_at=now
                )
                db.add(assignment)

        db.commit()

    except Exception as e:
        db.rollback()
        print(f"Error assigning tasks: {e}")


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
