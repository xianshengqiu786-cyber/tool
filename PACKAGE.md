# 打包成 EXE 指南

## 用户端需要安装的内容

### ✅ 好消息：基本不需要额外安装！

打包后的 EXE 文件是**独立可执行程序**，用户只需要：

1. **Windows 10/11 用户**：通常无需任何额外安装 ✅
2. **Windows 7/8 用户**：可能需要安装 [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### ❌ 不需要安装：
- Python
- pip
- 任何依赖包（mss、Pillow、PyQt5 都已打包）

---

## 开发者打包指南

### 1. 安装打包工具

```bash
pip install pyinstaller
```

### 2. 打包命令

#### 方法一：使用配置文件（推荐）
```bash
pyinstaller screenshot_tool.spec
```

#### 方法二：直接打包（简单）
```bash
# 基础打包
pyinstaller --onefile --windowed win1.py

# 带图标打包
pyinstaller --onefile --windowed --icon=icon.ico win1.py

# 自定义程序名
pyinstaller --onefile --windowed --name "ScreenshotTool" win1.py
```

### 3. 参数说明

| 参数 | 说明 |
|------|------|
| `--onefile` | 打包成单个 EXE 文件 |
| `--windowed` | 不显示控制台窗口（GUI 程序必须） |
| `--icon=icon.ico` | 添加程序图标 |
| `--name=NAME` | 自定义输出文件名 |
| `--add-data` | 添加额外数据文件 |

### 4. 打包后文件位置

```
tool/
├── build/          # 临时文件（可删除）
├── dist/           # 👈 打包后的 EXE 在这里
│   └── ScreenshotTool.exe
└── win1.py
```

### 5. 测试打包结果

```bash
# 进入 dist 目录
cd dist

# 运行测试
./ScreenshotTool.exe
```

---

## 常见问题

### Q1: 打包后 EXE 文件很大？
**A**: 正常现象。PyQt5 相关库较大，单个 EXE 通常在 30-50MB。可使用 UPX 压缩（但会增加启动时间）。

### Q2: 运行时提示"缺少 DLL"？
**A**: 用户电脑需要安装 [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)

### Q3: 杀毒软件报警？
**A**: PyInstaller 打包的程序可能被误报。可以：
- 签名程序（需要代码签名证书）
- 提前告知用户添加白名单

### Q4: 打包后无法运行？
**A**: 检查以下几点：
- 确保在打包前安装了所有依赖：`pip install -r requirements.txt`
- 尝试使用 `--console` 参数查看错误信息
- 检查杀毒软件是否拦截

---

## 分发给用户

### 最小化安装包方案

1. **只提供 EXE**（适用于 Windows 10/11）
   - 文件大小：~40MB
   - 用户直接双击运行

2. **EXE + VC++ Redistributable**（兼容 Windows 7/8）
   - 文件大小：~45MB
   - 包含 VC++ 运行时安装包

3. **在线安装方案**
   - 提供下载链接，用户从微软官网安装 VC++ 运行时
   - 减小分发包体积

---

## 推荐打包流程

```bash
# 1. 清理旧文件
rm -rf build dist

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装打包工具
pip install pyinstaller

# 4. 执行打包
pyinstaller screenshot_tool.spec

# 5. 测试
dist/ScreenshotTool.exe
```

---

## 高级选项

### 添加版本信息

创建 `version_info.txt`:
```
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Your Company'),
        StringStruct(u'FileDescription', u'Screenshot Tool'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'ScreenshotTool'),
        StringStruct(u'LegalCopyright', u'Copyright 2024'),
        StringStruct(u'OriginalFilename', u'ScreenshotTool.exe'),
        StringStruct(u'ProductName', u'Screenshot Tool'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
```

打包时添加：
```bash
pyinstaller --version-file=version_info.txt screenshot_tool.spec
```

---

## 快速开始

```bash
# 一键打包脚本
pip install pyinstaller && pyinstaller --onefile --windowed --name "ScreenshotTool" win1.py
```
