@echo off
chcp 65001 >nul
echo ======================================
echo     GUI 测试工具
echo ======================================
echo.

python test_gui.py

if errorlevel 1 (
    echo.
    echo [错误] GUI 测试失败
    echo.
    echo 可能的原因:
    echo 1. PyQt5 未安装
    echo 2. Python 版本过低
    echo.
    echo 解决方法:
    echo pip install PyQt5
    echo.
)

pause
