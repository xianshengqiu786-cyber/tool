"""
Windows 截图工具 - 简化版
功能：区域选择 → 截图 → 悬浮预览 → 保存/关闭
"""
import sys
import os
import platform
from datetime import datetime

# 检查系统
if platform.system() != "Windows":
    print("此版本仅支持 Windows 系统")
    sys.exit(1)

try:
    from PyQt5.QtWidgets import (QApplication, QWidget, QLabel,
                                  QPushButton, QVBoxLayout, QHBoxLayout,
                                  QFileDialog, QMessageBox)
    from PyQt5.QtCore import Qt, QPoint, QRect
    from PyQt5.QtGui import QPixmap, QPainter, QPen
except ImportError:
    print("错误: 未安装 PyQt5")
    print("请运行: pip install PyQt5")
    sys.exit(1)

# 注意：现在使用 PyQt5 的截图功能，不再需要 mss
# 但保留 mss 作为可选依赖（用于未来的扩展）
try:
    import mss
    MSS_AVAILABLE = True
except ImportError:
    MSS_AVAILABLE = False
    print("提示: mss 未安装（可选）")


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
            # 使用 PyQt5 的方法截屏（更可靠）
            app = QApplication.instance()
            if not app:
                app = QApplication([])

            # 获取主屏幕
            screen = QApplication.primaryScreen()

            # 截取整个屏幕（包括所有窗口）
            self.screen_pixmap = screen.grabWindow(0)  # 0 = 整个桌面

            # 保存到临时文件（为了后续使用）
            import tempfile
            self.temp_file = tempfile.mktemp(suffix='.png')
            self.screen_pixmap.save(self.temp_file)

            print(f"✓ 屏幕截图成功: {self.screen_pixmap.width()}x{self.screen_pixmap.height()}")

        except Exception as e:
            print(f"截图背景失败: {e}")
            import traceback
            traceback.print_exc()

            # 如果截图失败，获取屏幕尺寸并创建黑色背景
            screen = QApplication.desktop().screenGeometry()
            self.screen_pixmap = QPixmap(screen.width(), screen.height())
            self.screen_pixmap.fill(Qt.black)
            print(f"使用黑色背景: {screen.width()}x{screen.height()}")

    def paintEvent(self, event):
        """绘制背景和选择区域"""
        painter = QPainter(self)

        # 1. 先绘制屏幕截图作为背景
        if self.screen_pixmap:
            painter.drawPixmap(0, 0, self.screen_pixmap)

        # 2. 绘制半透明遮罩（让选择区域外变暗）
        if not self.start_pos.isNull() and not self.end_pos.isNull():
            selection = QRect(self.start_pos, self.end_pos).normalized()

            # 绘制半透明黑色遮罩
            painter.setBrush(Qt.black)
            painter.setPen(Qt.NoPen)
            painter.setOpacity(0.3)

            # 这里简化处理，只在整个窗口上绘制半透明层
            # 选择区域会在后面重新绘制为不透明

        # 3. 绘制选择框（红色边框）
        painter.setOpacity(1.0)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.setBrush(Qt.NoBrush)

        if not self.start_pos.isNull() and not self.end_pos.isNull():
            rect = QRect(self.start_pos, self.end_pos).normalized()
            painter.drawRect(rect)

            # 在选择框内显示尺寸信息
            size_text = f"{rect.width()} x {rect.height()}"
            painter.setPen(Qt.white)
            painter.drawText(rect.topLeft() + QPoint(5, -5), size_text)

    def mousePressEvent(self, event):
        """鼠标按下：开始选择"""
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()
            self.end_pos = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        """鼠标移动：更新选择区域"""
        if not self.start_pos.isNull():
            self.end_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """鼠标释放：完成选择"""
        if event.button() == Qt.LeftButton:
            self.end_pos = event.pos()
            self.selection_rect = QRect(self.start_pos, self.end_pos).normalized()
            print("区域选择完成！")
            self.cleanup_temp_file()
            self.close()

    def keyPressEvent(self, event):
        """按键事件：ESC 取消"""
        if event.key() == Qt.Key_Escape:
            print("已取消截图")
            self.selection_rect = None
            self.cleanup_temp_file()
            self.close()

    def cleanup_temp_file(self):
        """清理临时文件"""
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

        # 窗口标题
        self.setWindowTitle("截图预览")

        # 窗口标志：置顶 + 无边框
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        # 窗口大小
        self.resize(pixmap.width(), pixmap.height() + 60)

        # 鼠标拖动相关
        self.drag_position = None

        # 创建界面
        self.create_ui()

    def create_ui(self):
        """创建用户界面"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 1. 图片标签（可拖动）
        self.image_label = QLabel()
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #333;
                border: 2px solid #555;
            }
        """)
        layout.addWidget(self.image_label)

        # 2. 按钮栏
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(10, 10, 10, 10)

        # 保存按钮
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

        # 关闭按钮
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
        """鼠标按下：开始拖动"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        """鼠标移动：拖动窗口"""
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)

    def save_image(self):
        """保存截图"""
        # 生成默认文件名（带时间戳）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"截图_{timestamp}.png"

        # 获取桌面路径
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")

        # 文件保存对话框
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存截图",
            os.path.join(desktop_path, default_filename),
            "PNG 图片 (*.png);;所有文件 (*.*)"
        )

        if file_path:
            try:
                # 保存图片
                self.pixmap.save(file_path)

                # 显示成功提示
                QMessageBox.information(
                    self,
                    "保存成功",
                    f"截图已保存到:\n{file_path}"
                )

                # 关闭窗口
                self.close()

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "保存失败",
                    f"保存失败:\n{str(e)}"
                )


# ==================== 主程序 ====================
def main():
    """主程序入口"""

    # 创建应用
    app = QApplication(sys.argv)
    app.setApplicationName("Windows 截图工具")

    # 显示启动提示（1.5秒）
    print("=================================")
    print("  Windows 截图工具")
    print("=================================")
    print("正在启动...")
    print()

    # 1. 显示全屏选择窗口
    selector = ScreenSelector()
    selector.show()
    selector.raise_()
    selector.activateWindow()

    print("请按住鼠标左键拖动选择截图区域")
    print("按 ESC 键取消")
    print()

    # 等待选择完成
    while selector.isVisible():
        app.processEvents()

    # 检查是否选择了区域
    if not selector.selection_rect or selector.selection_rect.isEmpty():
        print("未选择区域，程序退出")
        return

    # 2. 从背景截图截取选中区域
    try:
        rect = selector.selection_rect

        print(f"截取区域: x={rect.x()}, y={rect.y()}, w={rect.width()}, h={rect.height()}")

        # 直接从已经截取的背景中获取选中区域
        # 这样可以确保内容和背景完全一致
        pixmap = selector.screen_pixmap.copy(rect.x(), rect.y(), rect.width(), rect.height())

        print(f"✓ 截图成功: {pixmap.width()}x{pixmap.height()}")

    except Exception as e:
        QMessageBox.critical(
            None,
            "截图失败",
            f"截图失败:\n{str(e)}"
        )
        print(f"错误详情: {e}")
        import traceback
        traceback.print_exc()
        return

    # 3. 显示悬浮预览窗口
    preview = FloatPreview(pixmap)
    preview.show()

    # 运行应用
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
