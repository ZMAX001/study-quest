from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_
from typing import List
from datetime import datetime

from app.database import get_db, Quest, UserQuest, User
from app.core.security import get_current_user
from app.schemas.quest import QuestResponse, UserQuestResponse, QuestProgress

router = APIRouter()

@router.get("/", response_model=List[QuestResponse])
async def get_quests(
    subject: str = None,
    difficulty: str = None,
    quest_type: str = None,
    db: AsyncSession = Depends(get_db)
):
    """获取任务列表"""
    query = select(Quest).where(Quest.is_active == True)
    
    if subject:
        query = query.where(Quest.subject == subject)
    if difficulty:
        query = query.where(Quest.difficulty == difficulty)
    if quest_type:
        query = query.where(Quest.quest_type == quest_type)
    
    result = await db.execute(query)
    quests = result.scalars().all()
    
    return [
        QuestResponse(
            id=quest.id,
            title=quest.title,
            description=quest.description,
            subject=quest.subject,
            difficulty=quest.difficulty,
            experience_reward=quest.experience_reward,
            gold_reward=quest.gold_reward,
            deadline=quest.deadline,
            quest_type=quest.quest_type,
            created_at=quest.created_at
        )
        for quest in quests
    ]

@router.get("/user", response_model=List[UserQuestResponse])
async def get_user_quests(
    current_user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户的任务列表"""
    query = select(UserQuest).where(UserQuest.user_id == current_user_id)
    result = await db.execute(query)
    user_quests = result.scalars().all()
    
    quest_responses = []
    for user_quest in user_quests:
        # 获取任务详情
        quest_result = await db.execute(select(Quest).where(Quest.id == user_quest.quest_id))
        quest = quest_result.scalar_one_or_none()
        
        if quest:
            quest_responses.append(UserQuestResponse(
                id=user_quest.id,
                quest_id=user_quest.quest_id,
                user_id=user_quest.user_id,
                is_completed=user_quest.is_completed,
                progress=user_quest.progress,
                score=user_quest.score,
                time_spent=user_quest.time_spent,
                attempts=user_quest.attempts,
                completed_at=user_quest.completed_at,
                created_at=user_quest.created_at,
                quest=QuestResponse(
                    id=quest.id,
                    title=quest.title,
                    description=quest.description,
                    subject=quest.subject,
                    difficulty=quest.difficulty,
                    experience_reward=quest.experience_reward,
                    gold_reward=quest.gold_reward,
                    deadline=quest.deadline,
                    quest_type=quest.quest_type,
                    created_at=quest.created_at
                )
            ))
    
    return quest_responses

@router.post("/start/{quest_id}")
async def start_quest(
    quest_id: int,
    current_user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """开始任务"""
    # 检查任务是否存在
    quest_result = await db.execute(select(Quest).where(Quest.id == quest_id))
    quest = quest_result.scalar_one_or_none()
    
    if not quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在"
        )
    
    # 检查用户是否已经有这个任务的记录
    existing_result = await db.execute(
        select(UserQuest).where(
            and_(UserQuest.user_id == current_user_id, UserQuest.quest_id == quest_id)
        )
    )
    existing_user_quest = existing_result.scalar_one_or_none()
    
    if existing_user_quest:
        # 更新尝试次数
        existing_user_quest.attempts += 1
        await db.commit()
        return {"message": "任务已开始", "user_quest_id": existing_user_quest.id}
    
    # 创建新的用户任务记录
    new_user_quest = UserQuest(
        user_id=current_user_id,
        quest_id=quest_id,
        attempts=1
    )
    
    db.add(new_user_quest)
    await db.commit()
    await db.refresh(new_user_quest)
    
    return {"message": "任务已开始", "user_quest_id": new_user_quest.id}

@router.put("/progress/{quest_id}")
async def update_quest_progress(
    quest_id: int,
    progress: QuestProgress,
    current_user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新任务进度"""
    # 查找用户任务记录
    user_quest_result = await db.execute(
        select(UserQuest).where(
            and_(UserQuest.user_id == current_user_id, UserQuest.quest_id == quest_id)
        )
    )
    user_quest = user_quest_result.scalar_one_or_none()
    
    if not user_quest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务记录不存在"
        )
    
    # 更新进度
    update_data = {}
    if progress.progress is not None:
        update_data["progress"] = progress.progress
    if progress.score is not None:
        update_data["score"] = progress.score
    if progress.time_spent is not None:
        update_data["time_spent"] = progress.time_spent
    
    # 检查是否完成
    if progress.progress and progress.progress >= 100:
        update_data["is_completed"] = True
        update_data["completed_at"] = datetime.utcnow()
        
        # 获取任务奖励
        quest_result = await db.execute(select(Quest).where(Quest.id == quest_id))
        quest = quest_result.scalar_one_or_none()
        
        if quest:
            # 更新用户经验值和金币
            user_result = await db.execute(select(User).where(User.id == current_user_id))
            user = user_result.scalar_one_or_none()
            
            if user:
                user.experience += quest.experience_reward
                user.gold_coins += quest.gold_reward
                
                # 检查是否升级
                new_level = (user.experience // 100) + 1
                if new_level > user.level:
                    user.level = new_level
    
    await db.execute(
        update(UserQuest)
        .where(UserQuest.id == user_quest.id)
        .values(**update_data)
    )
    await db.commit()
    
    return {"message": "进度已更新", "progress": progress.progress} 