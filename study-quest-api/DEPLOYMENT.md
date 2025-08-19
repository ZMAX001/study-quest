# Study Quest API 部署指南

## 部署到 Render

### 方式一：使用 render.yaml 自动部署（推荐）

1. **登录 Render 控制台**
   - 访问 [render.com](https://render.com)
   - 使用 GitHub 账号登录

2. **创建新服务**
   - 点击 "New" → "Blueprint"
   - 选择你的 GitHub 仓库
   - 选择 `study-quest-api` 分支
   - 点击 "Connect"

3. **自动配置**
   - Render 会自动读取 `render.yaml` 文件
   - 会创建两个服务：
     - `study-quest-api-dev` (开发版，无需数据库)
     - `study-quest-api-prod` (完整版，带数据库)

### 方式二：手动创建服务

#### 步骤 1：部署开发版本（快速验证）

1. **创建 Web Service**
   - New → Web Service
   - 选择你的 GitHub 仓库
   - Root Directory: `study-quest-api`
   - Environment: Python
   - Build Command: `pip install -r requirements-dev.txt`
   - Start Command: `uvicorn main-dev:app --host 0.0.0.0 --port $PORT`

2. **环境变量**
   - `PYTHON_VERSION`: `3.11.0`
   - `PORT`: `8000`

#### 步骤 2：创建数据库

1. **创建 PostgreSQL 数据库**
   - New → PostgreSQL
   - Name: `study-quest-db`
   - Database: `studyquest`
   - User: `studyquest_user`
   - Plan: Free

2. **获取连接字符串**
   - 在数据库详情页面复制 "External Database URL"
   - 格式：`postgresql://user:password@host:port/database`

#### 步骤 3：部署完整版本

1. **创建 Web Service**
   - New → Web Service
   - 选择你的 GitHub 仓库
   - Root Directory: `study-quest-api`
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

2. **环境变量**
   - `PYTHON_VERSION`: `3.11.0`
   - `PORT`: `8000`
   - `SECRET_KEY`: 生成一个随机字符串（至少32位）
   - `DATABASE_URL`: 从步骤2复制的数据库连接字符串

### 环境变量说明

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `PYTHON_VERSION` | Python 版本 | `3.11.0` |
| `PORT` | 服务端口 | `8000` |
| `SECRET_KEY` | JWT 签名密钥 | 随机32位字符串 |
| `DATABASE_URL` | 数据库连接字符串 | `postgresql://user:pass@host:port/db` |

### 部署后配置

1. **更新前端 API 地址**
   - 在 Vercel 中更新环境变量
   - 将 `VITE_API_BASE_URL` 改为你的 Render 服务地址

2. **测试 API 连接**
   - 访问 `https://your-service.onrender.com/docs`
   - 测试登录接口：`POST /auth/login`

### 注意事项

- **免费层限制**：
  - 服务空闲15分钟后会休眠
  - 冷启动需要30-60秒
  - 每月有使用时间限制

- **数据库限制**：
  - 免费 PostgreSQL 有30天试用期
  - 之后需要升级到付费计划或迁移到其他服务

- **建议**：
  - 先用开发版本快速上线验证
  - 功能稳定后再配置完整版本和数据库
  - 考虑使用 Supabase 或 Railway 作为数据库替代方案

## 本地开发

```bash
# 安装依赖
pip install -r requirements-dev.txt

# 启动开发服务器
python main-dev.py

# 或使用 uvicorn
uvicorn main-dev:app --reload --host 0.0.0.0 --port 8000
```

## 故障排除

1. **构建失败**：检查 requirements.txt 中的依赖版本
2. **启动失败**：检查环境变量和端口配置
3. **数据库连接失败**：验证 DATABASE_URL 格式和网络连接
4. **CORS 错误**：确保前端域名已添加到 CORS 配置中 