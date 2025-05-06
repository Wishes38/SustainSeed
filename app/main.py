from typing import Annotated
from fastapi import FastAPI, Request, Depends
from app.models import Base, User
from app.database import engine
from app.routers.auth import router as auth_router
from app.routers.eco_action import router as eco_action_router
from app.routers.daily_task import router as daily_task_router
from app.core.scheduler import scheduler
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from app.core.auth import decode_access_token
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.routers.home import router as home_router
from app.routers.logs import router as logs_router
from app.routers.chat import router as chat_router

templates = Jinja2Templates(directory="app/templates")

app = FastAPI()

scheduler.start()

app.mount("/static", StaticFiles(directory="app/static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    # 1) Cookie’den token
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/auth/login")

    # 2) Decode & kullanıcı yükle
    try:
        payload = decode_access_token(token)
        user_id = payload.get("id")
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User yok")
    except Exception:
        return RedirectResponse(url="/auth/login")

    # 3) xp yüzdesi (0–80 aralığında kalacak şekilde)
    xp_for_stage = user.xp % 80
    xp_percent = round(xp_for_stage / 80 * 100)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "user": {
            "first_name": user.first_name,
            "xp": user.xp,
            "percent": xp_percent,
            "plant_stage": user.plant_stage.value,
            "tree_count": user.tree_count
        }
    })


app.include_router(auth_router)
app.include_router(home_router)
app.include_router(eco_action_router)
app.include_router(daily_task_router)
app.include_router(logs_router)
app.include_router(chat_router)

Base.metadata.create_all(bind=engine)
