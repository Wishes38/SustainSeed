from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    first_name = str
    last_name = str
    xp: float
    level: int
    plant_stage: str

    class Config:
        orm_mode = True

class EcoActionCreate(BaseModel):
    description: str
    green_score: float
    xp_earned: float

class EcoActionRead(BaseModel):
    id: int
    description: str
    green_score: float
    xp_earned: float
    created_at: datetime

    class Config:
        orm_mode = True

class DailyTaskRead(BaseModel):
    id: int
    description: str
    green_score_estimate: float

    class Config:
        orm_mode = True

class UserTaskLogRead(BaseModel):
    id: int
    completed: bool
    created_at: datetime
    task: DailyTaskRead

    class Config:
        orm_mode = True

class PlantPersonaRead(BaseModel):
    id: int
    name: str
    mood: str
    motivational_quote: str

    class Config:
        orm_mode = True
