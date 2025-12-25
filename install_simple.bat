@echo off
echo ======================================
echo    Windows 截图工具 - 快速安装
echo ======================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python
    echo 请先安装 Python: https://www.python.org/downloads/
    echo.
    echo 安装时请勾选 "Add Python to PATH"
    pause
    exit /b 1
)

echo [1/3] 检查 Python 版本...
python --version

echo [2/3] 升级 pip...
python -m pip install --upgrade pip -q

echo [3/3] 安装依赖...
echo 只需要 PyQt5（约 50MB）
python -m pip install PyQt5 -q

echo.
echo ======================================
echo 安装完成！
echo.
echo 现在可以运行:
echo   python screenshot_simple.py
echo.
echo 或双击: 启动截图工具.bat
echo ======================================
echo.

pause
