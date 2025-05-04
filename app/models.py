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


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String(30))
    last_name = Column(String(30))
    phone_number = Column(String(20))
    role = Column(String(30))
    is_active = Column(Boolean, default=True)
    xp = Column(Float, default=0.0)
    plant_stage = Column(Enum(PlantStageEnum), default=PlantStageEnum.seed)
    tree_count = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    actions = relationship("EcoAction", back_populates="user")
    tasks = relationship("UserTaskLog", back_populates="user")

    def update_plant_stage(self):
        while self.xp >= 80:
            self.tree_count += 1
            self.xp -= 80

        if self.xp < 10:
            self.plant_stage = PlantStageEnum.seed
        elif self.xp < 20:
            self.plant_stage = PlantStageEnum.seedling
        elif self.xp < 35:
            self.plant_stage = PlantStageEnum.seedling_with_leaves
        elif self.xp < 50:
            self.plant_stage = PlantStageEnum.young_tree
        elif self.xp < 80:
            self.plant_stage = PlantStageEnum.growing_tree


class EcoAction(Base):
    __tablename__ = "eco_actions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(Text)
    description = Column(Text)
    xp_earned = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="actions")
    eco_action_logs = relationship("UserTaskLog", back_populates="eco_action_task")


class DailyTask(Base):
    __tablename__ = "daily_tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    description = Column(String)
    green_score_estimate = Column(Float)
    active = Column(Boolean, default=True)

    daily_logs = relationship("UserTaskLog", back_populates="daily_task")


class UserTaskLog(Base):
    __tablename__ = "user_task_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    daily_tasks = Column(Integer, ForeignKey("daily_task.id"))
    eco_action_id = Column(Integer, ForeignKey("eco_actions.id"))
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="tasks")
    daily_task = relationship("DailyTask", back_populates="daily_logs")
    eco_action_task = relationship("EcoAction", back_populates="eco_action_logs")
