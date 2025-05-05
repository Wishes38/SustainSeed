from sqlalchemy.orm import Session
from app.models import DailyTask, User, UserDailyTaskAssignment
from app.schemas import DailyTaskCreate


def create_and_assign_daily_task(db: Session, task_data: DailyTaskCreate) -> DailyTask:
    task = DailyTask(
        title=task_data.title,
        description=task_data.description,
        xp_earned=task_data.xp_earned,
        active=True,
    )
    db.add(task)
    db.commit()
    db.refresh(task)

    users = db.query(User).filter(User.is_active == True).all()

    for user in users:
        assignment = UserDailyTaskAssignment(
            user_id=user.id,
            daily_task_id=task.id,
            completed=False
        )
        db.add(assignment)

        user.xp += task_data.xp_earned
        while user.xp >= 80:
            user.tree_count += 1
            user.xp -= 80
        user.update_plant_stage()

    db.commit()
    return task
