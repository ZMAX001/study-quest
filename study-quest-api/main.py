from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
import asyncio
import uvicorn
from dotenv import load_dotenv
import os

from app.database import engine, Base
from app.routers import auth, users, quests, battles, rewards
from app.core.config import settings
from app.core.security import verify_token

# 加载环境变量
load_dotenv()

# 安全认证
security = HTTPBearer()

@asynccontextmanager
async def lifespan(app: FastAPI):
	# 启动时创建数据库表，带重试（适配无服务器与冷启动）
	retries = int(os.getenv("DB_INIT_RETRIES", "5"))
	delay_seconds = float(os.getenv("DB_INIT_DELAY", "1.5"))
	for attempt in range(1, retries + 1):
		try:
			async with engine.begin() as conn:
				await conn.run_sync(Base.metadata.create_all)
			print(f"[startup] database init succeeded on attempt {attempt}")
			break
		except Exception as exc:
			print(f"[startup] database init failed (attempt {attempt}/{retries}): {exc}")
			if attempt == retries:
				print("[startup] giving up database init after retries")
				raise
			await asyncio.sleep(delay_seconds)
	yield

# 创建FastAPI应用
app = FastAPI(
	title="Study Quest API",
	description="游戏化学习系统后端API",
	version="1.0.0",
	lifespan=lifespan
)

# 配置CORS
cors_origins_env = os.getenv("CORS_ORIGINS", "")
allowed_origins = [o.strip() for o in cors_origins_env.split(",") if o.strip()] or [
	"http://localhost:3000",
	"http://127.0.0.1:3000",
]
# 允许 vercel.app 子域
allow_origin_regex = os.getenv("CORS_ORIGIN_REGEX", r"https://.*\.vercel\.app$")

app.add_middleware(
	CORSMiddleware,
	allow_origins=allowed_origins,
	allow_origin_regex=allow_origin_regex,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# 依赖注入：获取当前用户
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
	try:
		payload = verify_token(credentials.credentials)
		user_id = payload.get("sub")
		if user_id is None:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="无效的认证凭据",
				headers={"WWW-Authenticate": "Bearer"},
			)
		return user_id
	except Exception:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="无效的认证凭据",
			headers={"WWW-Authenticate": "Bearer"},
		)

# 包含路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(users.router, prefix="/api/users", tags=["用户"])
app.include_router(quests.router, prefix="/api/quests", tags=["任务"])
app.include_router(battles.router, prefix="/api/battles", tags=["战斗"])
app.include_router(rewards.router, prefix="/api/rewards", tags=["奖励"])

@app.get("/")
async def root():
	return {"message": "Study Quest API 服务运行中"}

@app.get("/health")
async def health_check():
	return {"status": "healthy", "service": "Study Quest API"}

if __name__ == "__main__":
	uvicorn.run(
		"main:app",
		host="0.0.0.0",
		port=8000,
		reload=True,
		log_level="info"
	) 