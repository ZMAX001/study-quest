from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, func
from typing import List
from datetime import datetime

from app.database import get_db, User, RewardLog
from app.core.security import get_current_user

router = APIRouter()

@router.get("/history")
async def get_reward_history(
    current_user_id: int = Depends(get_current_user),
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """获取奖励历史记录"""
    query = select(RewardLog).where(RewardLog.user_id == current_user_id).order_by(RewardLog.created_at.desc())
    result = await db.execute(query.limit(limit))
    rewards = result.scalars().all()
    
    return [
        {
            "id": reward.id,
            "reward_type": reward.reward_type,
            "amount": reward.amount,
            "reason": reward.reason,
            "quest_id": reward.quest_id,
            "created_at": reward.created_at
        }
        for reward in rewards
    ]

@router.post("/exchange/game-time")
async def exchange_game_time(
    hours: int,
    current_user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """兑换游戏时间"""
    if hours <= 0 or hours > 4:  # 最多兑换4小时
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="兑换时间必须在1-4小时之间"
        )
    
    # 计算所需金币
    required_gold = hours * 30  # 1小时 = 30金币
    
    # 获取用户信息
    user_result = await db.execute(select(User).where(User.id == current_user_id))
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    if user.gold_coins < required_gold:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="金币不足"
        )
    
    # 扣除金币
    user.gold_coins -= required_gold
    
    # 记录奖励日志
    reward_log = RewardLog(
        user_id=current_user_id,
        reward_type="game_time",
        amount=hours,
        reason=f"兑换游戏时间 {hours} 小时"
    )
    
    db.add(reward_log)
    await db.commit()
    
    return {
        "message": f"成功兑换 {hours} 小时游戏时间",
        "gold_spent": required_gold,
        "remaining_gold": user.gold_coins,
        "game_time_hours": hours
    }

@router.get("/stats")
async def get_reward_stats(
    current_user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取奖励统计信息"""
    # 获取用户信息
    user_result = await db.execute(select(User).where(User.id == current_user_id))
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 获取今日获得的经验值
    today = datetime.utcnow().date()
    today_rewards = await db.execute(
        select(RewardLog).where(
            and_(
                RewardLog.user_id == current_user_id,
                RewardLog.reward_type == "experience",
                func.date(RewardLog.created_at) == today
            )
        )
    )
    today_experience = sum(reward.amount for reward in today_rewards.scalars().all())
    
    # 获取今日获得的金币
    today_gold = await db.execute(
        select(RewardLog).where(
            and_(
                RewardLog.user_id == current_user_id,
                RewardLog.reward_type == "gold",
                func.date(RewardLog.created_at) == today
            )
        )
    )
    today_gold_amount = sum(reward.amount for reward in today_gold.scalars().all())
    
    return {
        "current_level": user.level,
        "current_experience": user.experience,
        "current_gold": user.gold_coins,
        "experience_to_next_level": (user.level * 100) - user.experience,
        "level_progress": (user.experience % 100) / 100 * 100,
        "today_experience_gained": today_experience,
        "today_gold_gained": today_gold_amount
    } 