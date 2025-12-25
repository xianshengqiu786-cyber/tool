@echo off
chcp 65001 >nul
cls
echo ======================================
echo    Windows 截图工具 - 打包成 EXE
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

echo [1/6] 检查 Python 版本...
python --version
echo.

echo [2/6] 检查 PyQt5...
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo PyQt5 未安装，正在安装...
    pip install PyQt5 -q
    echo ✓ PyQt5 安装完成
) else (
    echo ✓ PyQt5 已安装
)
echo.

echo [3/6] 安装 PyInstaller...
python -m pip install pyinstaller -q
echo ✓ PyInstaller 准备就绪
echo.

echo [4/6] 测试源代码...
echo 正在运行测试...
python screenshot_simple.py
if errorlevel 1 (
    echo [警告] 源代码测试退出，但继续打包...
    echo.
)
echo.

echo [5/6] 清理旧文件...
if exist build rmdir /s /q build 2>nul
if exist dist rmdir /s /q dist 2>nul
echo ✓ 清理完成
echo.

echo [6/6] 开始打包...
echo 这可能需要 1-2 分钟，请耐心等待...
echo.
python -m PyInstaller simple.spec

echo.
echo ======================================
if exist "dist\ScreenshotTool.exe" (
    echo ✓ 打包成功！
    echo.
    echo 输出位置: dist\ScreenshotTool.exe
    echo.
    for %%A in ("dist\ScreenshotTool.exe") do (
        echo 文件大小: %%~zA 字节
    )
    echo.
    echo ======================================
    echo.
    echo 现在可以:
    echo 1. 进入 dist 文件夹
    echo 2. 双击 ScreenshotTool.exe 运行
    echo 3. 或将 EXE 发送给其他人使用
    echo.
) else (
    echo [错误] 打包失败
    echo.
    echo 可能的原因:
    echo 1. PyQt5 未正确安装
    echo 2. 源代码有错误
    echo.
    echo 请检查上面的错误信息
    echo ======================================
)

echo.
pause
