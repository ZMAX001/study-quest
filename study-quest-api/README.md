# Study Quest API

游戏化学习系统的后端API服务

## 技术栈

- **框架**: FastAPI
- **数据库**: PostgreSQL (异步)
- **ORM**: SQLAlchemy 2.0
- **认证**: JWT
- **密码加密**: bcrypt
- **异步支持**: asyncio

## 功能特性

- 用户认证与授权
- 任务管理系统
- 学习进度跟踪
- 奖励系统
- 排行榜功能
- 番茄钟学习记录

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 环境配置

创建 `.env` 文件：

```bash
# 数据库配置
DATABASE_URL=postgresql+asyncpg://username:password@localhost/study_quest

# JWT配置
SECRET_KEY=your-super-secret-key-here-change-in-production

# Redis配置
REDIS_URL=redis://localhost:6379

# 应用配置
DEBUG=true
```

### 3. 启动服务

```bash
python main.py
```

服务将在 http://localhost:8000 启动

### 4. API文档

访问 http://localhost:8000/docs 查看Swagger API文档

## API端点

### 认证
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/login-json` - JSON格式登录
- `GET /api/auth/me` - 获取当前用户信息

### 用户
- `GET /api/users/profile` - 获取用户资料
- `PUT /api/users/profile` - 更新用户资料
- `GET /api/users/stats` - 获取用户统计

### 任务
- `GET /api/quests/` - 获取任务列表
- `GET /api/quests/user` - 获取用户任务
- `POST /api/quests/start/{quest_id}` - 开始任务
- `PUT /api/quests/progress/{quest_id}` - 更新任务进度

### 战斗
- `GET /api/battles/leaderboard` - 获取排行榜
- `POST /api/battles/pomodoro-complete` - 完成番茄钟学习

### 奖励
- `GET /api/rewards/history` - 获取奖励历史
- `POST /api/rewards/exchange/game-time` - 兑换游戏时间
- `GET /api/rewards/stats` - 获取奖励统计

## 数据库模型

- **User**: 用户信息
- **Quest**: 任务定义
- **UserQuest**: 用户任务进度
- **StudyRecord**: 学习记录
- **RewardLog**: 奖励记录

## 开发说明

### 项目结构
```
app/
├── core/           # 核心配置
├── database.py     # 数据库配置和模型
├── routers/        # API路由
└── schemas/        # 数据模型
```

### 添加新功能
1. 在 `app/routers/` 中创建新的路由文件
2. 在 `app/schemas/` 中定义数据模型
3. 在 `main.py` 中注册新路由
4. 更新数据库模型（如需要）

## 部署

### Docker部署
```bash
docker build -t study-quest-api .
docker run -p 8000:8000 study-quest-api
```

### 生产环境
- 使用环境变量配置敏感信息
- 启用HTTPS
- 配置数据库连接池
- 设置日志记录
- 配置监控和健康检查

## 许可证

MIT License 