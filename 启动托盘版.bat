@echo off
chcp 65001 >nul
title Windows 截图工具 - 托盘版（无依赖）
cls
echo ======================================
echo  Windows 截图工具 - 托盘版
echo  （无需 keyboard 库）
echo ======================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python
    echo 请先安装 Python: https://www.python.org/licenses/
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
 echo - 使用 Windows 原生 API 注册热键
echo - 快捷键: Ctrl + Shift + S
echo - 双击托盘图标也可以截图
echo - 右键托盘图标显示菜单
echo.
echo 不需要 keyboard 库！
echo.
echo 正在启动...
echo.

start /B python screenshot_tray.py

timeout /t 2 >nul

echo.
echo ======================================
echo ✓ 程序已启动！
echo.
echo 查看右下角系统托盘图标
echo.
echo 使用方法:
echo - 快捷键: Ctrl + Shift + S
echo - 双击: 托盘图标
echo - 右键: 托盘图标菜单
echo ======================================
echo.

timeout /t 3 >nul
exit
