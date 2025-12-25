#!/bin/bash

echo "======================================"
echo "   Screenshot Tool - Build Script"
echo "======================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 Python3，请先安装 Python 3.7+"
    exit 1
fi

echo "[1/4] 检查依赖..."
if ! pip3 show pyinstaller &> /dev/null; then
    echo "正在安装 PyInstaller..."
    pip3 install pyinstaller
fi

echo "[2/4] 检查项目依赖..."
pip3 install -r requirements.txt

echo "[3/4] 清理旧文件..."
rm -rf build dist

echo "[4/4] 开始打包..."
pyinstaller screenshot_tool.spec

echo ""
echo "======================================"
echo "打包完成！"
echo "输出文件: dist/ScreenshotTool"
echo "======================================"
echo ""
