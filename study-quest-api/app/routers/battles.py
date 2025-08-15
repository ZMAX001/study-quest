from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List
from datetime import datetime

from app.database import get_db, User
from app.core.security import get_current_user

router = APIRouter()

@router.get("/leaderboard")
async def get_leaderboard(
    subject: str = None,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """获取排行榜"""
    query = select(User).where(User.is_active == True).order_by(User.experience.desc())
    
    if subject:
        # 这里可以根据学科过滤，需要额外的关联表
        pass
    
    result = await db.execute(query.limit(limit))
    users = result.scalars().all()
    
    leaderboard = []
    for i, user in enumerate(users, 1):
        leaderboard.append({
            "rank": i,
            "username": user.nickname or user.username,
            "level": user.level,
            "experience": user.experience,
            "gold_coins": user.gold_coins
        })
    
    return leaderboard

@router.post("/pomodoro-complete")
async def complete_pomodoro(
    subject: str,
    duration: int,
    current_user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """完成番茄钟学习"""
    # 获取用户
    user_result = await db.execute(select(User).where(User.id == current_user_id))
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 计算奖励
    experience_gain = (duration // 60) * 1  # 每分钟1经验
    gold_gain = (duration // 60) * 0.4  # 每分钟0.4金币
    
    # 更新用户数据
    user.experience += experience_gain
    user.gold_coins += int(gold_gain)
    
    # 检查是否升级
    new_level = (user.experience // 100) + 1
    if new_level > user.level:
        user.level = new_level
        # 升级奖励
        user.gold_coins += 50
    
    await db.commit()
    
    return {
        "message": "番茄钟学习完成",
        "experience_gained": experience_gain,
        "gold_gained": int(gold_gain),
        "new_level": user.level,
        "total_experience": user.experience,
        "total_gold": user.gold_coins
    } 