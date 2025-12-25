@echo off
echo ======================================
echo    启动 Windows 截图工具
echo ======================================
echo.

python screenshot_simple.py

if errorlevel 1 (
    echo.
    echo [错误] 程序运行出错
    echo.
    echo 请检查:
    echo 1. 是否安装了依赖: install_simple.bat
    echo 2. Python 版本是否为 3.8+
    echo.
)

pause
