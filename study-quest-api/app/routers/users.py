from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List

from app.database import get_db, User
from app.schemas.auth import UserResponse
from app.core.security import get_current_user

router = APIRouter()

@router.get("/profile", response_model=UserResponse)
async def get_user_profile(
    current_user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户个人资料"""
    result = await db.execute(select(User).where(User.id == current_user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        nickname=user.nickname,
        avatar=user.avatar,
        level=user.level,
        experience=user.experience,
        gold_coins=user.gold_coins,
        created_at=user.created_at
    )

@router.put("/profile", response_model=UserResponse)
async def update_user_profile(
    nickname: str = None,
    avatar: str = None,
    current_user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新用户个人资料"""
    update_data = {}
    if nickname is not None:
        update_data["nickname"] = nickname
    if avatar is not None:
        update_data["avatar"] = avatar
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="没有提供要更新的数据"
        )
    
    await db.execute(
        update(User)
        .where(User.id == current_user_id)
        .values(**update_data)
    )
    await db.commit()
    
    # 返回更新后的用户信息
    result = await db.execute(select(User).where(User.id == current_user_id))
    user = result.scalar_one_or_none()
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        nickname=user.nickname,
        avatar=user.avatar,
        level=user.level,
        experience=user.experience,
        gold_coins=user.gold_coins,
        created_at=user.created_at
    )

@router.get("/stats")
async def get_user_stats(
    current_user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取用户统计信息"""
    result = await db.execute(select(User).where(User.id == current_user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return {
        "level": user.level,
        "experience": user.experience,
        "gold_coins": user.gold_coins,
        "experience_to_next_level": (user.level * 100) - user.experience,
        "level_progress": (user.experience % 100) / 100 * 100
    } 