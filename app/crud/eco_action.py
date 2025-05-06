from sqlalchemy.orm import Session
from app.models import EcoAction, User, UserTaskLog
from app.ai.chat_bot import Chat
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

chat_log_bot = []
chat_log_user = []

chatbot = Chat(GEMINI_API_KEY, "gemini-2.5-flash-preview-04-17", chat_log_bot, chat_log_user)


def create_eco_action(db: Session, user_id: int) -> EcoAction:
    temp = chatbot.get_response("Bana bir görev ver.", None, None, None, None)
    task = temp["content"]
    title = task["title"]
    description = task["description"]
    xp_value = task.get("xp_earned", 5.0)

    eco_action = EcoAction(
        user_id=user_id,
        title=title,
        description=description,
        xp_earned=xp_value,
    )
    db.add(eco_action)
    db.flush()

    log = UserTaskLog(
        user_id=user_id,
        eco_action_id=eco_action.id,
        completed=False
    )
    db.add(log)

    user = db.query(User).get(user_id)
    if user:
        user.xp += xp_value
        while user.xp >= 80:
            user.tree_count += 1
            user.xp -= 80
        user.update_plant_stage()

    db.commit()
    db.refresh(eco_action)
    return eco_action


def get_eco_actions_by_user(db: Session, user_id: int):
    return (
        db.query(EcoAction)
        .filter(EcoAction.user_id == user_id)
        .order_by(EcoAction.created_at.desc())
        .all()
    )


def complete_eco_action(db: Session, user_id: int, eco_action_id: int) -> bool:
    log = (
        db.query(UserTaskLog)
        .filter_by(user_id=user_id, eco_action_id=eco_action_id)
        .first()
    )
    if not log:
        log = UserTaskLog(user_id=user_id, eco_action_id=eco_action_id, completed=True)
        db.add(log)
    elif log.completed:
        return False
    else:
        log.completed = True

    action = db.get(EcoAction, eco_action_id)
    user = db.get(User, user_id)
    if action and user:
        user.xp += action.xp_earned
        user.update_plant_stage()

    db.commit()
    return True


def uncomplete_eco_action(db: Session, user_id: int, eco_action_id: int) -> bool:
    log = (
        db.query(UserTaskLog)
        .filter_by(user_id=user_id, eco_action_id=eco_action_id)
        .first()
    )
    if not log or not log.completed:
        return False

    log.completed = False

    action = db.get(EcoAction, eco_action_id)
    user = db.get(User, user_id)
    if action and user:
        user.xp = max(user.xp - action.xp_earned, 0)
        while user.xp < 0 and user.tree_count > 0:
            user.tree_count -= 1
            user.xp += 80
        user.update_plant_stage()

    db.commit()
    return True
