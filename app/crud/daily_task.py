from sqlalchemy.orm import Session
from datetime import datetime, UTC
from app.models import DailyTask, UserDailyTaskAssignment, User
from app.schemas import DailyTaskCreate
from sqlalchemy import cast, Date
from sqlalchemy import cast, Date
from app.ai.chat_bot import Chat
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

chat_log_bot = []
chat_log_user = []

chatbot = Chat(GEMINI_API_KEY, "gemini-2.5-flash-preview-04-17", chat_log_bot, chat_log_user)

user_time_frame, user_location, current_time = "Tüm gün içinde yapabileceğim", "Herhangi bir yer olabilir, farketmez.", "Günün herhangi bir vaktinde"

def create_daily_task(db: Session, task_data: DailyTaskCreate) -> DailyTask:

    temp=chatbot.get_response("Bana bir görev ver.",None,user_time_frame, user_location, current_time)
    print(temp)
    new_task = DailyTask(
        title=temp["content"]["title"],
        description=temp["content"]["description"],
        xp_earned=7.0
    )

    print(new_task)
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


def uncomplete_task(db: Session, assignment_id: int, user_id: int):
    assignment = db.query(UserDailyTaskAssignment)\
        .filter_by(id=assignment_id, user_id=user_id)\
        .first()

    if assignment and assignment.completed:
        assignment.completed = False

        task = db.query(DailyTask).get(assignment.daily_task_id)
        user = db.query(User).get(user_id)
        if task and user:
            user.xp = max(user.xp - task.xp_earned, 0)
            user.update_plant_stage()

        db.commit()
        db.refresh(assignment)
        return assignment

    return None
