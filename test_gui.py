"""
简单的 GUI 测试脚本
用于诊断 PyQt5 是否能正常工作
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI 测试")
        self.resize(400, 200)
        self.setStyleSheet("background-color: #2b2b2b; color: white;")

        layout = QVBoxLayout()

        # 标题
        title = QLabel("✅ PyQt5 运行正常！")
        title.setFont(QFont("Arial", 16))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # 说明
        info = QLabel("如果你能看到这个窗口，\n说明 PyQt5 已经正确安装。")
        info.setAlignment(Qt.AlignCenter)
        layout.addWidget(info)

        # 按钮
        btn = QPushButton("关闭测试")
        btn.clicked.connect(self.close)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(btn)

        self.setLayout(layout)

def main():
    print("正在启动 GUI 测试...")

    app = QApplication(sys.argv)

    window = TestWindow()
    window.show()

    print("✅ GUI 窗口已显示")
    print("如果看不到窗口，可能被其他程序遮挡")
    print("检查任务栏是否有新窗口")

    sys.exit(app.exec_())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 错误: {e}")
        input("按 Enter 退出...")
