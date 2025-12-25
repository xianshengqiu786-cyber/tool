@echo off
echo ======================================
echo    Screenshot Tool - Build Script
echo ======================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.7+
    pause
    exit /b 1
)

echo [1/4] 检查依赖...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 正在安装 PyInstaller...
    pip install pyinstaller
)

echo [2/4] 检查项目依赖...
pip install -r requirements.txt

echo [3/4] 清理旧文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo [4/4] 开始打包...
pyinstaller screenshot_tool.spec

echo.
echo ======================================
echo 打包完成！
echo 输出文件: dist\ScreenshotTool.exe
echo ======================================
echo.

pause
