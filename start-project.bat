@echo off
echo ========================================
echo        Study Quest 项目启动脚本
echo ========================================
echo.

echo 正在启动前端开发服务器...
cd study-quest-web
start "Study Quest Frontend" cmd /k "npm run dev"
cd ..

echo.
echo 正在启动后端API服务器 (开发版)...
cd study-quest-api
start "Study Quest Backend Dev" cmd /k "python main-dev.py"
cd ..

echo.
echo ========================================
echo 项目启动完成！
echo.
echo 前端: http://localhost:3000
echo 后端: http://localhost:8000
echo API文档: http://localhost:8000/docs
echo.
echo 注意: 后端使用开发版本，无需数据库配置
echo ========================================
echo.
echo 按任意键退出...
pause > nul 