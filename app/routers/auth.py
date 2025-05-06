from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated
from app.database import SessionLocal
from app.models import User
from app.schemas import CreateUserRequest, Token, UserUpdate, UserRead
from app.core.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
current_user_dependency = Annotated[dict, Depends(lambda token: decode_access_token(token))]


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


@router.post("/login", response_model=Token)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Hatalı Kullanıcı Adı yada Şifre")

    token = create_access_token({
        "sub": user.username,
        "id": user.id,
        "role": user.role
    })
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
def get_current_user_info(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency):
    payload = decode_access_token(token)
    user = db.query(User).filter(User.id == payload.get("id")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/me", response_model=UserRead)
def update_current_user_info(
        user_update: UserUpdate,
        token: Annotated[str, Depends(oauth2_scheme)],
        db: db_dependency
):
    payload = decode_access_token(token)
    user = db.query(User).filter(User.id == payload.get("id")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for attr, value in user_update.dict(exclude_unset=True).items():
        setattr(user, attr, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency):
    payload = decode_access_token(token)
    user = db.query(User).filter(User.id == payload.get("id")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted"}


@router.post("/update-xp")
def update_user_xp(xp_amount: float, db: db_dependency, token: Annotated[str, Depends(oauth2_scheme)]):
    payload = decode_access_token(token)
    user = db.query(User).filter(User.id == payload.get("id")).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    user.xp += xp_amount
    user.update_plant_stage()

    db.commit()
    db.refresh(user)

    return {
        "message": "XP updated successfully.",
        "new_xp": user.xp,
        "plant_stage": user.plant_stage.value,
        "tree_count": user.tree_count
    }


@router.get("/logout", name="auth_logout")
async def logout():
    response = RedirectResponse(url="/auth/login")
    response.delete_cookie(key="access_token", path="/")
    return response

@router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

