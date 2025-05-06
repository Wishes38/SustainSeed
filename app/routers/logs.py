from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List, Annotated
from app.database import SessionLocal
from app.core.auth import decode_access_token
from app.models import UserTaskLog
from app.schemas import UserTaskLogRead

router = APIRouter(prefix="/user-task-logs", tags=["User Task Logs"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


token_dep = Annotated[str, Depends(oauth2_scheme)]
db_dep = Annotated[Session, Depends(get_db)]


@router.get("/", response_model=List[UserTaskLogRead])
def list_user_task_logs(
        token: token_dep,
        db: db_dep
):
    payload = decode_access_token(token)
    if not payload or "id" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_id = payload["id"]

    return (
        db.query(UserTaskLog)
        .filter(UserTaskLog.user_id == user_id)
        .all()
    )
