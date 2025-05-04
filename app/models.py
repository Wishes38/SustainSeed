from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class PlantStageEnum(enum.Enum):
    seed = "seed"
    seedling = "seedling"
    seedling_with_leaves = "seedling_with_leaves"
    young_tree = "young_tree"
    growing_tree = "growing_tree"
    mature_tree = "mature_tree"

class MoodEnum(enum.Enum):
    happy = "happy"
    sad = "sad"
    neutral = "neutral"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String(20))
    role = Column(String)
    is_active = Column(Boolean, default=True)
    xp = Column(Float, default=0.0)
    level = Column(Integer, default=1)
    plant_stage = Column(Enum(PlantStageEnum), default=PlantStageEnum.seed)
    tree_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    actions = relationship("EcoAction", back_populates="user")
    tasks = relationship("UserTaskLog", back_populates="user")

    @property
    def plant_stage(self):
        if self.xp < 10:
            return PlantStageEnum.seed
        elif self.xp < 20:
            return PlantStageEnum.seedling
        elif self.xp < 35:
            return PlantStageEnum.seedling_with_leaves
        elif self.xp < 50:
            return PlantStageEnum.young_tree
        elif self.xp < 80:
            return PlantStageEnum.growing_tree
        else:
            self.tree_count += 1
            self.xp = 0
            return PlantStageEnum.mature_tree

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
    mood = Column(Enum(MoodEnum), default=MoodEnum.neutral)
    motivational_quote = Column(String)
