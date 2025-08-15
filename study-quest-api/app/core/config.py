from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # 应用配置
    app_name: str = "Study Quest API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # 数据库配置
    database_url: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/study_quest")
    
    # JWT配置
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Redis配置
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # 跨域配置
    allowed_origins: list = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # 文件上传配置
    upload_dir: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    
    # 游戏配置
    pomodoro_duration: int = 25 * 60  # 25分钟
    experience_per_pomodoro: int = 25
    gold_per_pomodoro: int = 10
    
    class Config:
        env_file = ".env"

settings = Settings() 