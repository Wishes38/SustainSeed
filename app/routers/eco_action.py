from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import SessionLocal
from app.schemas import EcoActionCreate, EcoActionRead
from app.core.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from app.crud import eco_action as eco_action_crud


router = APIRouter(
    prefix="/eco-actions",
    tags=["Eco Actions"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=EcoActionRead)
def create_action(
    action_data: EcoActionCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_data = decode_access_token(token)
    if not user_data or "id" not in user_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return eco_action_crud.create_eco_action(db, user_id=user_data["id"], action_data=action_data)


@router.get("/", response_model=List[EcoActionRead])
def get_my_eco_actions(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_data = decode_access_token(token)
    if not user_data or "id" not in user_data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return eco_action_crud.get_eco_actions_by_user(db, user_id=user_data["id"])
