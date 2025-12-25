import sys
import os
import platform
import subprocess

import mss
from PIL import Image

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QFileDialog
)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
from PyQt5.QtCore import Qt, QRect, QPoint

# 临时截图文件
if platform.system() == "Windows":
    TEMP_IMG = os.path.join(os.environ['USERPROFILE'], "temp_screenshot.png")
else:
    TEMP_IMG = os.path.expanduser("~/temp_screenshot.png")


# ================= 区域选择窗口 =================
class AreaSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.start = QPoint()
        self.end = QPoint()
        self.selection = None

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowState(Qt.WindowFullScreen)
        self.setCursor(Qt.CrossCursor)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2))
        painter.setBrush(Qt.transparent)
        if not self.start.isNull() and not self.end.isNull():
            painter.drawRect(QRect(self.start, self.end).normalized())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = event.pos()
            self.end = event.pos()
            self.update()

    def mouseMoveEvent(self, event):
        if not self.start.isNull():
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.end = event.pos()
            self.selection = QRect(self.start, self.end).normalized()
            self.close()


# ================= 钉图窗口 =================
class PinWindow(QWidget):
    def __init__(self, pixmap):
        super().__init__()
        self.setWindowTitle("截图预览")
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

        layout = QVBoxLayout(self)

        self.label = QLabel()
        self.label.setPixmap(pixmap)
        layout.addWidget(self.label)

        btn_save = QPushButton("保存")
        btn_save.clicked.connect(lambda: self.save_image(pixmap))

        btn_close = QPushButton("关闭")
        btn_close.clicked.connect(self.close)

        layout.addWidget(btn_save)
        layout.addWidget(btn_close)

        self.resize(pixmap.width(), pixmap.height() + 60)

        self.old_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def save_image(self, pixmap):
        path, _ = QFileDialog.getSaveFileName(
            self, "保存截图",
            os.path.expanduser("~/Desktop"),
            "PNG Files (*.png)"
        )
        if path:
            pixmap.save(path)
            self.close()


# ================= 主流程 =================
def capture_area():
    system = platform.system()

    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)

    # -------- macOS --------
    if system == "Darwin":
        if os.path.exists(TEMP_IMG):
            os.remove(TEMP_IMG)

        subprocess.run(["screencapture", "-i", TEMP_IMG])
        if not os.path.exists(TEMP_IMG):
            return

        pixmap = QPixmap(TEMP_IMG)
        win = PinWindow(pixmap)
        win.show()
        sys.exit(app.exec_())

    # -------- Windows --------
    else:
        # Windows: 需要设置 DPI 感知
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except:
            pass

        selector = AreaSelector()
        selector.show()

        # ✅ 直接运行主循环
        app.exec_()

        if not selector.selection:
            return

        rect = selector.selection

        # 获取屏幕信息，处理多显示器情况
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        # 截图 - 需要考虑 DPI 缩放
        with mss.mss() as sct:
            # 获取主显示器信息
            monitor = sct.monitors[1]  # monitors[0] 是虚拟屏幕，monitors[1] 是主显示器

            # 计算实际坐标（考虑 DPI 缩放）
            device_pixel_ratio = screen.devicePixelRatio()

            monitor = {
                "left": int(rect.x() / device_pixel_ratio),
                "top": int(rect.y() / device_pixel_ratio),
                "width": int(rect.width() / device_pixel_ratio),
                "height": int(rect.height() / device_pixel_ratio),
            }

            # 确保坐标在有效范围内
            monitor["left"] = max(0, monitor["left"])
            monitor["top"] = max(0, monitor["top"])

            sct_img = sct.grab(monitor)

            img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
            img.save(TEMP_IMG)

        pixmap = QPixmap(TEMP_IMG)
        win = PinWindow(pixmap)
        win.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    capture_area()
