from sqlalchemy.orm import Session
from app.models import EcoAction, User
from app.schemas import EcoActionCreate


def create_eco_action(db: Session, user_id: int, action_data: EcoActionCreate) -> EcoAction:
    eco_action = EcoAction(
        user_id=user_id,
        description=action_data.description,
        green_score=action_data.green_score,
        xp_earned=action_data.xp_earned,
    )
    db.add(eco_action)

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
    return db.query(EcoAction).filter(EcoAction.user_id == user_id).order_by(EcoAction.created_at.desc()).all()
