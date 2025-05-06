from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.ai.chat_bot import Chat
from sqlalchemy.orm import Session
from app.models import EcoAction, User, UserTaskLog
from app.database import SessionLocal
from fastapi import Depends
import os
from dotenv import load_dotenv

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


chat_log_bot = []
chat_log_user = []

chatbot = Chat(GEMINI_API_KEY, "gemini-2.5-flash-preview-04-17", chat_log_bot, chat_log_user)


@router.post("/", response_model=dict)
def chat_with_bot(request: ChatRequest, db: Session = Depends(get_db)):
    user = db.query(User).first()
    player_plane_level = user.plant_stage.value

    result = chatbot.get_response(request.message, player_plane_level)

    if result["type"] == "task":
        return {
            "mode": "task",
            "task": result["content"]
        }
    else:
        return {
            "mode": "chat",
            "message": result["content"]
        }
