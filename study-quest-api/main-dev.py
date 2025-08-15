from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import uvicorn
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 安全认证
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 开发版本，不需要数据库初始化
    yield

# 创建FastAPI应用
app = FastAPI(
    title="Study Quest API (开发版)",
    description="游戏化学习系统后端API - 开发版本",
    version="1.0.0-dev",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模拟用户数据
mock_users = {
    "student": {"id": 1, "username": "student", "role": "student", "nickname": "学生", "level": 1, "experience": 0, "gold_coins": 100},
    "parent": {"id": 2, "username": "parent", "role": "parent", "nickname": "家长", "level": 1, "experience": 0, "gold_coins": 0},
    "teacher": {"id": 3, "username": "teacher", "role": "teacher", "nickname": "教师", "level": 1, "experience": 0, "gold_coins": 0}
}

# 模拟任务数据
mock_quests = [
    {"id": 1, "title": "数学函数基础", "description": "学习函数概念", "subject": "数学", "difficulty": "easy", "experience_reward": 50, "gold_reward": 10},
    {"id": 2, "title": "英语阅读理解", "description": "阅读短文练习", "subject": "英语", "difficulty": "medium", "experience_reward": 80, "gold_reward": 15},
    {"id": 3, "title": "物理力学基础", "description": "牛顿运动定律", "subject": "物理", "difficulty": "medium", "experience_reward": 70, "gold_reward": 12}
]

@app.get("/")
async def root():
    return {"message": "Study Quest API 开发版服务运行中", "status": "development"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Study Quest API Dev", "database": "mock"}

# 认证相关API
@app.post("/api/auth/login-json")
async def login_json(username: str, password: str, role: str = None):
    """简化的用户登录"""
    if username in mock_users and password == "123456":
        user = mock_users[username]
        return {
            "access_token": f"mock-token-{user['id']}",
            "token_type": "bearer",
            "user_id": user["id"],
            "username": user["username"],
            "role": user["role"]
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

@app.get("/api/auth/me")
async def get_current_user_info(authorization: str = Depends(security)):
    """获取当前用户信息"""
    # 简化的token验证
    token = authorization.credentials
    if token.startswith("mock-token-"):
        user_id = int(token.split("-")[-1])
        for user in mock_users.values():
            if user["id"] == user_id:
                return {
                    "id": user["id"],
                    "username": user["username"],
                    "role": user["role"],
                    "nickname": user["nickname"],
                    "level": user["level"],
                    "experience": user["experience"],
                    "gold_coins": user["gold_coins"]
                }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭据"
    )

# 任务相关API
@app.get("/api/quests/")
async def get_quests(subject: str = None, difficulty: str = None):
    """获取任务列表"""
    filtered_quests = mock_quests
    if subject:
        filtered_quests = [q for q in filtered_quests if q["subject"] == subject]
    if difficulty:
        filtered_quests = [q for q in filtered_quests if q["difficulty"] == difficulty]
    
    return filtered_quests

@app.get("/api/quests/user")
async def get_user_quests(authorization: str = Depends(security)):
    """获取用户任务列表"""
    # 模拟用户任务数据
    return [
        {
            "id": 1,
            "quest_id": 1,
            "user_id": 1,
            "is_completed": False,
            "progress": 60.0,
            "score": None,
            "time_spent": 300,
            "attempts": 1,
            "completed_at": None,
            "created_at": "2024-01-01T00:00:00Z",
            "quest": mock_quests[0]
        }
    ]

# 战斗系统API
@app.get("/api/battles/leaderboard")
async def get_leaderboard(subject: str = None, limit: int = 10):
    """获取排行榜"""
    return [
        {"rank": 1, "username": "学霸小王", "level": 5, "experience": 450, "gold_coins": 200},
        {"rank": 2, "username": "学习达人", "level": 4, "experience": 380, "gold_coins": 180},
        {"rank": 3, "username": "知识探索者", "level": 4, "experience": 320, "gold_coins": 150}
    ]

@app.post("/api/battles/pomodoro-complete")
async def complete_pomodoro(subject: str, duration: int, authorization: str = Depends(security)):
    """完成番茄钟学习"""
    experience_gain = (duration // 60) * 1
    gold_gain = (duration // 60) * 0.4
    
    return {
        "message": f"番茄钟学习完成，学习了 {subject}",
        "experience_gained": experience_gain,
        "gold_gained": int(gold_gain),
        "subject": subject,
        "duration": duration
    }

# 奖励系统API
@app.get("/api/rewards/stats")
async def get_reward_stats(authorization: str = Depends(security)):
    """获取奖励统计信息"""
    return {
        "current_level": 1,
        "current_experience": 0,
        "current_gold": 100,
        "experience_to_next_level": 100,
        "level_progress": 0.0,
        "today_experience_gained": 0,
        "today_gold_gained": 0
    }

if __name__ == "__main__":
    print("🚀 启动 Study Quest API 开发版...")
    print("📖 API文档: http://localhost:8000/docs")
    print("🔍 健康检查: http://localhost:8000/health")
    print("⚠️  注意: 这是开发版本，使用模拟数据")
    
    uvicorn.run(
        "main-dev:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 