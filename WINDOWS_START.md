# Windows 上如何运行此程序

## 📋 方法一：拷贝 .py 脚本运行（推荐给有 Python 基础的用户）

### 第 0 步：确认已安装 Python

打开 CMD（命令提示符），输入：
```bash
python --version
```

如果显示版本号（如 Python 3.11.x），说明已安装 ✅

如果提示"不是内部或外部命令"，需要先安装 Python：
- 下载：https://www.python.org/downloads/
- ⚠️ **安装时必须勾选 "Add Python to PATH"**
- 重启 CMD

---

### 第 1 步：拷贝文件到 Windows

只需要复制这 **1 个文件**：
```
screenshot_simple.py  ← 主程序
```

**可选文件**（如果需要）：
```
requirements_simple.txt  ← 依赖列表（手动安装时需要）
run.bat                  ← 快速启动脚本
```

---

### 第 2 步：安装依赖

#### 方法 A：自动安装（推荐）

在 CMD 中进入脚本所在目录，运行：
```bash
pip install PyQt5 mss Pillow
```

等待安装完成（大约 1-2 分钟）

#### 方法 B：使用 requirements 文件

```bash
pip install -r requirements_simple.txt
```

---

### 第 3 步：运行程序

#### 方法 A：直接运行 Python 脚本

在 CMD 中运行：
```bash
python screenshot_simple.py
```

#### 方法 B：双击运行（需要 .bat 文件）

双击 `run.bat` 文件（如果有的话）

---

## 📦 方法二：打包成 EXE（推荐给普通用户）

### 优点
- ✅ 无需安装 Python
- ✅ 无需安装依赖
- ✅ 双击直接运行
- ✅ 可以分发给其他人

### 步骤

#### 1. 拷贝文件到 Windows

需要复制这些文件：
```
screenshot_simple.py      ← 主程序
simple.spec              ← 打包配置
build_simple.bat         ← 打包脚本
```

#### 2. 安装 PyInstaller

```bash
pip install pyinstaller
```

#### 3. 运行打包脚本

双击 `build_simple.bat`

或手动运行：
```bash
pyinstaller simple.spec
```

#### 4. 获取 EXE 文件

打包完成后，在这里找到 EXE 文件：
```
dist\ScreenshotTool.exe
```

#### 5. 运行 EXE

双击 `ScreenshotTool.exe` 即可运行！

---

## 🎯 推荐方案对比

| 方案 | 优点 | 缺点 | 适合人群 |
|------|------|------|----------|
| **直接运行 .py** | 文件小（几KB）<br>修改方便 | 需要安装 Python<br>需要安装依赖 | 开发者<br>有 Python 基础 |
| **打包成 EXE** | 无需 Python<br>双击运行<br>可分发 | 文件大（30-40MB）<br>不能修改代码 | 普通用户<br>生产环境 |

---

## 📝 完整操作示例

### 场景：你想在另一台 Windows 电脑上运行

#### 方案 A：复制 .py 脚本

```bash
# 1. 复制文件到 U 盘或发送到目标电脑
screenshot_simple.py

# 2. 在目标电脑上打开 CMD
# 3. 安装依赖（只需一次）
pip install PyQt5 mss Pillow

# 4. 运行程序
python screenshot_simple.py
```

#### 方案 B：打包成 EXE 后分发

```bash
# 1. 在你的电脑上打包
build_simple.bat

# 2. 复制 EXE 文件到 U 盘
dist\ScreenshotTool.exe

# 3. 在目标电脑上双击运行
# (无需安装任何东西)
```

---

## ⚠️ 常见问题

### Q1: 提示 "python 不是内部或外部命令"

**A**: 没有安装 Python 或环境变量没配置

解决：
1. 安装 Python：https://www.python.org/downloads/
2. 重启 CMD
3. 再次运行 `python --version` 检查

### Q2: 提示 "No module named 'PyQt5'"

**A**: 依赖没有安装

解决：
```bash
pip install PyQt5 mss Pillow
```

### Q3: 运行 .py 脚本时一闪而过

**A**: 这是正常现象，程序启动后会隐藏控制台

如果要看错误信息，修改 `run.bat`：
```batch
@echo off
python screenshot_simple.py
pause
```

### Q4: EXE 文件太大，能压缩吗？

**A**: 可以尝试 UPX 压缩，但效果有限。30-40MB 是正常大小（包含 PyQt5）。

### Q5: 杀毒软件拦截怎么办？

**A**: 误报，添加到白名单或临时关闭杀毒软件

---

## 🚀 快速开始（3 步）

### 如果已有 Python

```bash
# 1. 复制 screenshot_simple.py 到任意文件夹
# 2. 打开 CMD，进入该文件夹
# 3. 运行
pip install PyQt5 mss Pillow && python screenshot_simple.py
```

### 如果没有 Python

```bash
# 1. 安装 Python（勾选 Add to PATH）
# 2. 重启 CMD
# 3. 运行
pip install PyQt5 mss Pillow && python screenshot_simple.py
```

---

## 💡 最佳实践

**开发时**：运行 .py 脚本（方便修改和调试）
**分发时**：打包成 EXE（用户友好）

---

## 📁 文件结构

**最小运行包（运行 .py）：**
```
MyFolder/
  └── screenshot_simple.py     ← 只需要这一个！
```

**完整开发包：**
```
MyFolder/
  ├── screenshot_simple.py      ← 主程序
  ├── requirements_simple.txt  ← 依赖列表
  ├── run.bat                   ← 启动脚本
  └── SIMPLE_GUIDE.md           ← 使用说明
```

**打包后（给用户）：**
```
只需发送：ScreenshotTool.exe
```

---

## 🎉 总结

**最简单的方法（推荐）：**

1. 复制 `screenshot_simple.py` 到 Windows
2. 安装依赖：`pip install PyQt5 mss Pillow`
3. 运行：`python screenshot_simple.py`

**或者直接打包成 EXE：**

1. 运行 `build_simple.bat`
2. 分发 `dist\ScreenshotTool.exe`
3. 用户双击运行

就这么简单！
