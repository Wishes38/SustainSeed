from sqlalchemy.orm import Session
from app.models import EcoAction, User, UserTaskLog
from app.schemas import EcoActionCreate
from sqlalchemy.exc import NoResultFound


def create_eco_action(db: Session, user_id: int, action_data: EcoActionCreate) -> EcoAction:
    eco_action = EcoAction(
        user_id=user_id,
        title=action_data.title,
        description=action_data.description,
        xp_earned=action_data.xp_earned,
    )
    db.add(eco_action)
    db.flush()

    log = UserTaskLog(
        user_id=user_id,
        eco_action_id=eco_action.id,
        completed=False
    )
    db.add(log)

    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.xp += action_data.xp_earned
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


def complete_eco_action(db: Session, user_id: int, eco_action_id: int):
    log = (
        db.query(UserTaskLog)
        .filter(
            UserTaskLog.user_id == user_id,
            UserTaskLog.eco_action_id == eco_action_id,
        )
        .first()
    )
    if not log:
        raise NoResultFound("EcoAction log not found for this user")

    log.completed = True
    db.commit()
    db.refresh(log)
    return log
