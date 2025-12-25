@echo off
chcp 65001 >nul
title Windows 截图工具 - 改进热键版
cls
echo ======================================
echo  Windows 截图工具 - 改进热键版
echo  （修复热键消息处理）
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
echo 功能说明:
echo - 改进的热键消息处理
echo - 快捷键: Ctrl + Shift + S
echo - 备用: Ctrl + Shift + X
echo - 双击托盘图标也可以截图
echo - 右键托盘图标显示菜单
echo.
echo 提示:
echo - 如果热键不工作，请以管理员身份运行
echo - 或使用双击托盘图标
echo.
echo 正在启动...
echo.

start /B python screenshot_tray_fixed.py

timeout /t 2 >nul

echo.
echo ======================================
echo ✓ 程序已启动！
echo.
echo 查看控制台窗口查看热键注册状态
echo.
echo 快捷键:
echo   • Ctrl + Shift + S
echo   • Ctrl + Shift + X
echo.
echo 托盘操作:
echo   • 双击托盘图标
echo   • 右键托盘图标 → 菜单
echo.
echo 如果热键不工作:
echo   1. 以管理员身份运行此脚本
echo   2. 或使用双击托盘图标
echo ======================================
echo.

timeout /t 3 >nul
exit
