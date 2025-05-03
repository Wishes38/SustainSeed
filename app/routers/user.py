from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.schemas import UserCreate, UserRead, UserUpdate
from app.crud.user import create_user as crud_create_user, get_user, get_users, update_user, delete_user
from typing import List, Annotated

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
def create_user_route(user: UserCreate, db: db_dependency):
    db_user = crud_create_user(db, user)
    print(f"AAAAAAAAAAAAAAABBBBBBB:  {db_user}")
    if not db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return db_user


@router.get("/", response_model=List[UserRead])
def get_users_route(db: db_dependency, skip: int = 0, limit: int = 100):
    users = get_users(db, skip, limit)
    return users


@router.get("/{user_id}", response_model=UserRead)
def get_user_route(user_id: int, db: db_dependency):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=UserUpdate)
def update_user_route(user_id: int, user: UserUpdate, db: db_dependency):
    db_user = update_user(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(user_id: int, db: db_dependency):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
