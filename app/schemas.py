from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    phone_number: str
    plant_stage: str
    is_active: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    phone_number: Optional[str] = None

    class Config:
        orm_mode = True


class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: EmailStr
    first_name: str
    last_name: str
    role: str
    phone_number: str


class Token(BaseModel):
    access_token: str
    token_type: str


class EcoActionCreate(BaseModel):
    title: str
    description: str
    xp_earned: float


class EcoActionRead(BaseModel):
    id: int
    user_id: int
    title: Optional[str]
    description: Optional[str]
    xp_earned: float
    created_at: datetime

    class Config:
        orm_mode = True


class DailyTaskBase(BaseModel):
    title: str
    description: str
    xp_earned: float


class DailyTaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class DailyTaskRead(BaseModel):
    id: int
    title: str
    description: Optional[str]
    xp_earned: float

    class Config:
        orm_mode = True


class AssignmentRead(BaseModel):
    id: int
    daily_task_id: int
    completed: bool
    assigned_at: datetime
    daily_task: DailyTaskRead

    class Config:
        orm_mode = True
