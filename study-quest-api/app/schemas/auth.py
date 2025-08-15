from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    password: str
    role: str = "student"  # student, parent, teacher
    nickname: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str
    role: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str
    role: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    role: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    level: int
    experience: int
    gold_coins: int
    created_at: datetime

    class Config:
        from_attributes = True 