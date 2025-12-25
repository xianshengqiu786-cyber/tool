"""
Windows 截图工具 - 托盘版（无需快捷键库）
功能：系统托盘 + Windows 原生热键 API
特点：无需 keyboard 库，使用 Windows API 注册热键
"""
import sys
import os
import platform
from datetime import datetime
import ctypes
from ctypes import wintypes

# 检查系统
if platform.system() != "Windows":
    print("此版本仅支持 Windows 系统")
    sys.exit(1)

try:
    from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                                  QPushButton, QVBoxLayout, QHBoxLayout,
                                  QFileDialog, QMessageBox, QSystemTrayIcon,
                                  QMenu, QAction)
    from PyQt5.QtCore import Qt, QPoint, QRect
    from PyQt5.QtGui import QPixmap, QPainter, QPen, QIcon, QKeySequence
except ImportError:
    print("错误: 未安装 PyQt5")
    print("请运行: pip install PyQt5")
    sys.exit(1)

# ==================== Windows 热键 API ====================
user32 = ctypes.windll.user32

# Windows 常量
MOD_CONTROL = 0x0002
MOD_ALT = 0x0001
MOD_SHIFT = 0x0004
VK_S = 0x53  # S键
VK_F9 = 0x78  # F9键
WM_HOTKEY = 0x0312

# 注册热键函数
def register_hotkey(hwnd, id, modifiers, vk):
    """注册Windows热键"""
    return user32.RegisterHotKey(hwnd, id, modifiers, vk)

# 取消注册热键
def unregister_hotkey(hwnd, id):
    """取消Windows热键"""
    return user32.UnregisterHotKey(hwnd, id)


# ==================== 区域选择窗口 ====================
class ScreenSelector(QWidget):
    """全屏区域选择窗口"""

    def __init__(self):
        super().__init__()
        self.start_pos = QPoint()
        self.end_pos = QPoint()
        self.selection_rect = None
        self.screen_pixmap = None

        # 先截取整个屏幕作为背景
        self.capture_screen()

        # 设置窗口属性
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setCursor(Qt.CrossCursor)

        # 显示全屏
        screen = QApplication.desktop().screenGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())

    def capture_screen(self):
        """截取整个屏幕作为背景"""
        try:
            app = QApplication.instance()
            if not app:
                app = QApplication([])

            screen = QApplication.primaryScreen()
            self.screen_pixmap = screen.grabWindow(0)

            import tempfile
            self.temp_file = tempfile.mktemp(suffix='.png')
            self.screen_pixmap.save(self.temp_file)

            print(f"✓ 屏幕截图成功: {self.screen_pixmap.width()}x{self.screen_pixmap.height()}")

        except Exception as e:
            print(f"截图背景失败: {e}")
            import traceback
            traceback.print_exc()

            screen = QApplication.desktop().screenGeometry()
            self.screen_pixmap = QPixmap(screen.width(), screen.height())
            self.screen_pixmap.fill(Qt.black)
            print(f"使用黑色背景: {screen.width()}x{screen.height()}")

    def paintEvent(self, event):
        """绘制背景和选择区域"""
        painter = QPainter(self)

        if self.screen_pixmap:
            painter.drawPixmap(0, 0, self.screen_pixmap)

        painter.setOpacity(1.0)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.setBrush(Qt.NoBrush)

        if not self.start_pos.isNull() and not self.end_pos.isNull():
            rect = QRect(self.start_pos, self.end_pos).normalized()
            painter.drawRect(rect)

            size_text = f"{rect.width()} x {rect.height()}"
            painter.setPen(Qt.white)
            painter.drawText(rect.topLeft() + QPoint(5, -5), size_text)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()
            self.end_pos = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if not self.start_pos.isNull():
            self.end_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end_pos = event.pos()
            self.selection_rect = QRect(self.start_pos, self.end_pos).normalized()
            print("区域选择完成！")
            self.cleanup_temp_file()
            self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            print("已取消截图")
            self.selection_rect = None
            self.cleanup_temp_file()
            self.close()

    def cleanup_temp_file(self):
        try:
            if hasattr(self, 'temp_file') and os.path.exists(self.temp_file):
                os.remove(self.temp_file)
        except:
            pass


# ==================== 悬浮预览窗口 ====================
class FloatPreview(QWidget):
    """悬浮预览窗口"""

    def __init__(self, pixmap):
        super().__init__()
        self.pixmap = pixmap

        self.setWindowTitle("截图预览")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.resize(pixmap.width(), pixmap.height() + 60)
        self.drag_position = None

        self.create_ui()

    def create_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel()
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #333;
                border: 2px solid #555;
            }
        """)
        layout.addWidget(self.image_label)

        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10, 10, 10, 10)

        self.save_btn = QPushButton("💾 保存")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.save_btn.clicked.connect(self.save_image)
        button_layout.addWidget(self.save_btn)

        self.close_btn = QPushButton("✖ 关闭")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)

        layout.addLayout(button_layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)

    def save_image(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"截图_{timestamp}.png"
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存截图",
            os.path.join(desktop_path, default_filename),
            "PNG 图片 (*.png);;所有文件 (*.*)"
        )

        if file_path:
            try:
                self.pixmap.save(file_path)
                QMessageBox.information(self, "保存成功", f"截图已保存到:\n{file_path}")
                self.close()
            except Exception as e:
                QMessageBox.critical(self, "保存失败", f"保存失败:\n{str(e)}")


# ==================== 系统托盘应用（Windows API 版）====================
class ScreenshotApp:
    """截图应用主类（使用 Windows API 热键）"""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Windows 截图工具")
        self.app.setQuitOnLastWindowClosed(False)

        # 创建隐藏窗口用于接收热键消息
        from PyQt5.QtWidgets import QWidget
        self.hotkey_window = QWidget()
        self.hotkey_window.setWindowFlags(Qt.FramelessWindowHint)
        self.hotkey_window.setGeometry(0, 0, 1, 1)
        self.hotkey_window.show()

        # 获取窗口句柄
        import ctypes
        hwnd = int(self.hotkey_window.winId())

        # 注册热键
        self.hotkey_registered = False
        self.register_windows_hotkeys(hwnd)

        # 创建托盘图标
        self.create_tray_icon()

        print("=" * 50)
        print("  Windows 截图工具 - 托盘版（无依赖）")
        print("=" * 50)
        print(f"✓ 程序已启动，最小化到系统托盘")
        if self.hotkey_registered:
            print(f"✓ 热键已注册: Ctrl + Shift + S")
        else:
            print(f"⚠️  热键注册失败，请使用托盘菜单")
        print(f"✓ 双击托盘图标也可以截图")
        print("=" * 50)
        print()

    def register_windows_hotkeys(self, hwnd):
        """使用 Windows API 注册热键"""
        try:
            # 注册 Ctrl + Shift + S
            # ID=1, Ctrl+Shift, S键
            result = register_hotkey(hwnd, 1, MOD_CONTROL | MOD_SHIFT, VK_S)

            if result:
                print("✓ 热键 Ctrl+Shift+S 已注册（Windows API）")
                self.hotkey_registered = True
            else:
                print("⚠️  热键注册失败，可能被占用")
                self.hotkey_registered = False

        except Exception as e:
            print(f"⚠️  热键注册错误: {e}")
            self.hotkey_registered = False

    def create_tray_icon(self):
        """创建系统托盘图标"""
        self.tray_icon = QSystemTrayIcon()

        icon = self.app.style().standardIcon(self.app.style().SP_ComputerIcon)
        self.tray_icon.setIcon(icon)

        # 创建托盘菜单
        menu = QMenu()

        # 截图动作（大字体突出显示）
        screenshot_action = QAction("📸 截图 (双击托盘图标)", None)
        screenshot_action.triggered.connect(self.start_screenshot)
        menu.addAction(screenshot_action)

        menu.addSeparator()

        # 测试热键
        if self.hotkey_registered:
            test_action = QAction("🔧 测试热键", None)
            test_action.triggered.connect(self.test_hotkey)
            menu.addAction(test_action)

        menu.addSeparator()

        # 退出动作
        quit_action = QAction("✖ 退出", None)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)

        # 设置托盘提示
        if self.hotkey_registered:
            self.tray_icon.setToolTip("Windows 截图工具\n热键: Ctrl + Shift + S\n双击托盘图标也可以截图")
        else:
            self.tray_icon.setToolTip("Windows 截图工具\n双击托盘图标截图\n热键不可用")

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.show()

        # 双击托盘图标也可以截图
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # 显示启动提示
        if self.hotkey_registered:
            msg = "程序已启动！\n热键: Ctrl + Shift + S\n双击托盘图标也可以截图"
        else:
            msg = "程序已启动！\n双击托盘图标截图\n热键不可用（请使用托盘菜单）"

        self.tray_icon.showMessage("截图工具", msg, QSystemTrayIcon.Information, 3000)

    def tray_icon_activated(self, reason):
        """托盘图标被激活（双击）"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.start_screenshot()

    def test_hotkey(self):
        """测试热键"""
        QMessageBox.information(
            None,
            "热键测试",
            "热键功能：\n\n按下 Ctrl + Shift + S\n应该会触发截图\n\n如果没反应，请：\n1. 检查是否被其他软件占用\n2. 使用双击托盘图标截图"
        )

    def start_screenshot(self):
        """开始截图"""
        print("\n[截图] 触发截图...")

        selector = ScreenSelector()
        selector.show()
        selector.raise_()
        selector.activateWindow()

        print("请按住鼠标左键拖动选择截图区域")
        print("按 ESC 键取消")

        while selector.isVisible():
            self.app.processEvents()

        if not selector.selection_rect or selector.selection_rect.isEmpty():
            print("未选择区域，已取消")
            return

        try:
            rect = selector.selection_rect

            print(f"截取区域: x={rect.x()}, y={rect.y()}, w={rect.width()}, h={rect.height()}")

            pixmap = selector.screen_pixmap.copy(rect.x(), rect.y(), rect.width(), rect.height())

            print(f"✓ 截图成功: {pixmap.width()}x{pixmap.height()}")

            preview = FloatPreview(pixmap)
            preview.show()

            preview.exec_()

            print("✓ 截图完成")

        except Exception as e:
            QMessageBox.critical(None, "截图失败", f"截图失败:\n{str(e)}")
            print(f"错误详情: {e}")
            import traceback
            traceback.print_exc()

    def quit_app(self):
        """退出应用"""
        print("\n退出程序...")

        # 取消注册热键
        if self.hotkey_registered:
            try:
                hwnd = int(self.hotkey_window.winId())
                unregister_hotkey(hwnd, 1)
            except:
                pass

        self.tray_icon.hide()
        self.hotkey_window.close()
        self.app.quit()

    def run(self):
        """运行应用"""
        return self.app.exec_()


# ==================== 主程序 ====================
def main():
    """主程序入口"""
    app = ScreenshotApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
