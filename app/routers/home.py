# app/routers/home.py
from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.core.auth import decode_access_token

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db: Session):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = decode_access_token(token)
        return db.query(User).get(payload.get("id"))
    except:
        return None

def build_user_dict(user: User):
    xp_for_stage = user.xp % 80
    percent = round(xp_for_stage / 80 * 100)
    return {
        "first_name": user.first_name,
        "xp": user.xp,
        "percent": percent,
        "plant_stage": user.plant_stage.value,
        "tree_count": user.tree_count
    }

@router.get("/", name="home")
async def overview(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/auth/login")
    return templates.TemplateResponse("index.html", {
        "request": request,
        "user": build_user_dict(user)
    })

@router.get("/profile", name="profile")
async def profile(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/auth/login")
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": build_user_dict(user)
    })

@router.get("/tasks", name="tasks")
async def tasks(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/auth/login")
    # burada görevler için ek data gelebilir
    return templates.TemplateResponse("tasks.html", {
        "request": request,
        "user": build_user_dict(user)
    })

@router.get("/settings", name="settings")
async def settings(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/auth/login")
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "user": build_user_dict(user)
    })

@router.get("/about", name="about")
async def about(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/auth/login")
    return templates.TemplateResponse("about.html", {
        "request": request,
        "user": build_user_dict(user)
    })
