from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuestResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    subject: str
    difficulty: str
    experience_reward: int
    gold_reward: int
    deadline: Optional[datetime] = None
    quest_type: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserQuestResponse(BaseModel):
    id: int
    quest_id: int
    user_id: int
    is_completed: bool
    progress: float
    score: Optional[int] = None
    time_spent: int
    attempts: int
    completed_at: Optional[datetime] = None
    created_at: datetime
    quest: QuestResponse

    class Config:
        from_attributes = True

class QuestProgress(BaseModel):
    progress: Optional[float] = None
    score: Optional[int] = None
    time_spent: Optional[int] = None

class QuestCreate(BaseModel):
    title: str
    description: Optional[str] = None
    subject: str
    difficulty: str = "medium"
    experience_reward: int = 0
    gold_reward: int = 0
    deadline: Optional[datetime] = None
    quest_type: str = "daily" 