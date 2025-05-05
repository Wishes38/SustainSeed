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


@app.get("/", response_class=templates.TemplateResponse)
async def home(request: Request, db: db_dependency):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/auth/login")
    try:

        payload = decode_access_token(token)
        user_id = payload.get("id")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("Invalid user")
    except Exception:

        return RedirectResponse(url="/auth/login")

    context = {
        "request": request,
        "title": "Anasayfa",
        "user": {"name": user.username, "xp": user.xp}
    }
    return templates.TemplateResponse("index.html", context)


app.include_router(auth_router)
app.include_router(eco_action_router)
app.include_router(daily_task_router)

Base.metadata.create_all(bind=engine)
