@echo off
chcp 65001 >nul
title Windows 截图工具
cls
echo ======================================
echo     Windows 截图工具
echo ======================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python
    echo.
    echo 请先安装 Python:
    echo 1. 访问 https://www.python.org/downloads/
    echo 2. 下载并安装 Python 3.8 或更高版本
    echo 3. ⚠️ 安装时必须勾选 "Add Python to PATH"
    echo 4. 安装完成后重启此程序
    echo.
    pause
    exit /b 1
)

echo [1/4] 检查 Python 版本...
python --version
echo.

echo [2/4] 检查依赖...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖，请稍候...
    echo.
    echo 只需要 PyQt5（约 50MB，请耐心等待）
    pip install PyQt5 -q
    echo.
    echo ✓ 依赖安装完成
) else (
    echo ✓ 依赖已安装
)
echo.

echo [3/4] 启动截图工具...
echo.
echo 提示:
echo - 屏幕会变暗（黑色半透明）
echo - 按住鼠标左键拖动选择区域
echo - 松开鼠标完成截图
echo - 按 ESC 键取消
echo.
echo 正在启动...
echo.

python screenshot_simple.py

echo.
echo [4/4] 程序已退出
echo.
pause
