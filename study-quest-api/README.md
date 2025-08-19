# Study Quest API

该目录包含基于 FastAPI 的后端服务。

## 本地运行（开发版）

```bash
pip install -r requirements-dev.txt
uvicorn main-dev:app --reload --host 0.0.0.0 --port 8000
```

## 本地运行（完整版本）

```bash
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 部署

### Vercel（免服务器部署）

已提供 Vercel 所需配置：
- `api/index.py`：导出 `app`
- `vercel.json`：指定 Python 运行时 3.11 和路由到 `api/index.py`

在 Vercel 控制台：
- Import Git → 选择仓库
- Framework Preset: Other
- Root Directory: `study-quest-api`
- Build Command:（留空）
- Output Directory:（留空）
- 环境变量：
  - `SECRET_KEY`：至少32位随机字符串
  - 如使用数据库：`DATABASE_URL`（示例：`postgresql+asyncpg://USER:PASSWORD@HOST:PORT/DB?sslmode=require`）
  - 可选：`CORS_ORIGINS`、`CORS_ORIGIN_REGEX`

部署完成后访问：`https://your-project.vercel.app/docs`

注意：Vercel 免费层为无状态函数，连接数据库建议使用 Serverless（例如 Neon、Supabase），并使用 `?sslmode=require`。

### Render（可选）

详见 `DEPLOYMENT.md` 或 `render.yaml` Blueprint。 