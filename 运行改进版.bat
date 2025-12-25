@echo off
chcp 65001 >nul
title Windows 截图工具 - 改进热键版（调试模式）
cls
echo ======================================
echo  Windows 截图工具 - 改进热键版
echo  （调试模式 - 保留控制台）
echo ======================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python
    echo 请先安装 Python: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/2] 检查依赖...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo 正在安装 PyQt5（约 50MB，请耐心等待）...
    pip install PyQt5 -q
    echo ✓ PyQt5 安装完成
) else (
    echo ✓ PyQt5 已安装
)
echo.

echo [2/2] 启动截图工具...
echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║  调试模式 - 保留控制台窗口查看详细输出         ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo 功能说明:
echo • 改进的热键消息处理
echo • 快捷键: Ctrl + Shift + S
echo • 备用: Ctrl + Shift + X
echo • 双击托盘图标也可以截图
echo.
echo 调试信息:
echo • 控制台会显示热键注册状态
echo • 按快捷键时会显示检测信息
echo • 按 Ctrl+C 可以停止程序
echo.
echo 正在启动...
echo ======================================
echo.

python screenshot_tray_fixed.py

echo.
echo ======================================
echo 程序已退出
echo.
pause
