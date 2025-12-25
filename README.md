# 跨平台截图工具

一个基于 PyQt5 的跨平台截图工具，支持 macOS 和 Windows 系统。

## 功能特性

- **macOS**: 使用系统自带的 `screencapture` 命令进行交互式截图
- **Windows**: 使用自定义区域选择窗口 + mss 库进行截图
- 支持区域选择预览
- 支持拖拽移动预览窗口
- 支持保存截图到本地

## 系统要求

- Python 3.7+
- macOS 10.14+ 或 Windows 10+

## 安装依赖

```bash
pip install -r requirements.txt
```

依赖包：
- `mss` - 跨平台屏幕截图库
- `Pillow` - Python 图像处理库
- `PyQt5` - GUI 框架

## 使用方法

### macOS

```bash
python win1.py
```

运行后会调用系统截图工具，选择区域后会自动在预览窗口中显示。

### Windows

```bash
python win1.py
```

1. 运行后会显示全屏红色边框选择窗口
2. 按住鼠标左键拖拽选择截图区域
3. 释放鼠标后自动截图并显示预览窗口
4. 点击"保存"按钮保存截图
5. 点击"关闭"按钮关闭预览窗口

## Windows 特别说明

- 已优化 DPI 缩放支持，适用于高分辨率屏幕
- 已处理多显示器情况，默认在主显示器截图
- 如遇权限问题，请尝试以管理员身份运行

## 文件说明

- `win1.py` - 主程序文件
- `win.py` - 旧版本（仅作备份）
- `requirements.txt` - 依赖列表
- `screenshot_tool.spec` - PyInstaller 打包配置
- `build.bat` - Windows 打包脚本
- `build.sh` - macOS/Linux 打包脚本

## 打包成 EXE

### 用户端无需安装 Python！

打包后的 EXE 文件是独立的可执行程序：

- ✅ Windows 10/11：直接运行，无需任何额外安装
- ⚠️ Windows 7/8：可能需要 [VC++ 运行时](https://aka.ms/vs/17/release/vc_redist.x64.exe)

详细打包教程请查看：[PACKAGE.md](PACKAGE.md)

### 快速打包

**Windows:**
```bash
build.bat
```

**macOS/Linux:**
```bash
./build.sh
```

或手动执行：
```bash
pip install pyinstaller
pyinstaller screenshot_tool.spec
```

打包后的文件在 `dist/ScreenshotTool.exe`

用户使用指南请查看：[USER_GUIDE.md](USER_GUIDE.md)

## 技术细节

### Windows 截图流程

1. 设置 Windows DPI 感知模式
2. 显示全屏透明选择窗口
3. 用户选择区域后获取坐标
4. 根据 DPI 缩放计算实际坐标
5. 使用 mss 库截取指定区域
6. 显示预览窗口

### macOS 截图流程

1. 删除旧的临时截图文件
2. 调用 `screencapture -i` 命令
3. 用户交互式选择区域
4. 读取截图文件并显示预览

## 已知问题

- Windows 多显示器环境下，跨显示器截图可能不准确
- macOS 依赖系统命令，无法自定义选择窗口样式

## 许可证

MIT License
