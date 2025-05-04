from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated
from app.database import SessionLocal
from app.models import User
from app.schemas import CreateUserRequest, Token
from app.core.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: CreateUserRequest, db: db_dependency):
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists.")

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        hashed_password=hash_password(user_data.password),
        role=user_data.role,
        phone_number=user_data.phone_number,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully."}


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({
        "sub": user.username,
        "id": user.id,
        "role": user.role
    })
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_access_token(token)
    return {
        "username": payload.get("sub"),
        "user_id": payload.get("id"),
        "role": payload.get("role")
    }
