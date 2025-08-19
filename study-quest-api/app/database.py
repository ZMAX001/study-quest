from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator
import os

# 数据库URL（建议使用 Supabase/Neon 的连接串，并包含 ?sslmode=require）
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/study_quest")

# 创建异步引擎（无服务器环境：禁用连接池与 prepared statements）
engine = create_async_engine(
    DATABASE_URL,
    echo=bool(os.getenv("SQL_ECHO", "")),
    poolclass=NullPool,
    connect_args={
        # 关闭 asyncpg 的语句缓存，避免在 PgBouncer 下出现 prepared statement 错误
        "statement_cache_size": 0,
    },
)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 创建基类
Base = declarative_base()

# 数据库依赖
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# 用户模型
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="student")  # student, parent, teacher
    nickname = Column(String(50), nullable=True)
    avatar = Column(String(255), nullable=True)
    level = Column(Integer, default=1)
    experience = Column(Integer, default=0)
    gold_coins = Column(Integer, default=100)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# 任务模型
class Quest(Base):
    __tablename__ = "quests"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String(50), nullable=False)
    difficulty = Column(String(20), default="medium")  # easy, medium, hard
    experience_reward = Column(Integer, default=0)
    gold_reward = Column(Integer, default=0)
    deadline = Column(DateTime(timezone=True), nullable=True)
    quest_type = Column(String(20), default="daily")  # daily, weekly, boss, special
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# 用户任务进度模型
class UserQuest(Base):
    __tablename__ = "user_quests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quest_id = Column(Integer, ForeignKey("quests.id"), nullable=False)
    is_completed = Column(Boolean, default=False)
    progress = Column(Float, default=0.0)  # 0.0 - 100.0
    score = Column(Integer, nullable=True)
    time_spent = Column(Integer, default=0)  # 秒
    attempts = Column(Integer, default=0)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# 学习记录模型
class StudyRecord(Base):
    __tablename__ = "study_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subject = Column(String(50), nullable=False)
    duration = Column(Integer, nullable=False)  # 秒
    study_type = Column(String(20), default="pomodoro")  # pomodoro, quest, battle
    quest_id = Column(Integer, ForeignKey("quests.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# 奖励记录模型
class RewardLog(Base):
    __tablename__ = "reward_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reward_type = Column(String(50), nullable=False)  # experience, gold, item
    amount = Column(Integer, nullable=False)
    reason = Column(String(200), nullable=True)
    quest_id = Column(Integer, ForeignKey("quests.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 