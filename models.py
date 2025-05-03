from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base  # database.py içinde SQLAlchemy Base tanımı olduğunu varsayıyorum

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    xp = Column(Float, default=0.0)
    level = Column(Integer, default=1)
    plant_stage = Column(String, default="seed")  # seed / sprout / flower

    actions = relationship("EcoAction", back_populates="user")
    tasks = relationship("UserTaskLog", back_populates="user")


class EcoAction(Base):
    __tablename__ = "eco_actions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(Text)
    green_score = Column(Float)
    xp_earned = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="actions")


class DailyTask(Base):
    __tablename__ = "daily_tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    green_score_estimate = Column(Float)
    active = Column(Boolean, default=True)

    logs = relationship("UserTaskLog", back_populates="task")


class UserTaskLog(Base):
    __tablename__ = "user_task_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("daily_tasks.id"))
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="tasks")
    task = relationship("DailyTask", back_populates="logs")


class PlantPersona(Base):
    __tablename__ = "plant_personas"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    mood = Column(String)  # happy / sad / neutral
    motivational_quote = Column(String)
