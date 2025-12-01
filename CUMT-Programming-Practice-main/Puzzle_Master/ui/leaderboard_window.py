import json
import os
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton, QTableWidget
from PyQt5.QtGui import QFont, QPalette, QBrush, QPixmap
from PyQt5.QtCore import Qt
from utils.styles import LeaderboardStyles


class LeaderboardWindow(QMainWindow):
    """排行榜窗口"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("排行榜")
        self.resize(500, 400)
        # 设置窗口整体背景色
        self.setStyleSheet("background-color: #f0f0f0;")
        self.leaderboard_data = []
        self.load_leaderboard()
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 设置中央窗口部件的背景色，确保没有黑色区域
        central_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(240, 240, 240, 0.95);
                border-radius: 5px;
            }
        """)

        background_path = "background.jpg"
        if os.path.exists(background_path):
            palette = QPalette()
            pixmap = QPixmap(background_path)
            scaled_pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
            central_widget.setPalette(palette)
            central_widget.setAutoFillBackground(True)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        title_label = QLabel("挑战模式排行榜")
        title_font = QFont("Arial", 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(LeaderboardStyles.TITLE_STYLE)
        main_layout.addWidget(title_label)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["排名", "时间(秒)", "步数", "日期"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet(LeaderboardStyles.TABLE_STYLE)
        main_layout.addWidget(self.table)

        self.populate_table()

        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet(LeaderboardStyles.CLOSE_BUTTON)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

    def load_leaderboard(self):
        """加载排行榜数据"""
        self.leaderboard_data = []
        if os.path.exists("leaderboard.json"):
            try:
                with open("leaderboard.json", "r", encoding="utf-8") as f:
                    self.leaderboard_data = json.load(f)
                self.leaderboard_data.sort(key=lambda x: x["time"])
            except:
                self.leaderboard_data = []

    def populate_table(self):
        """填充表格数据"""
        self.table.setRowCount(len(self.leaderboard_data))
        for i, record in enumerate(self.leaderboard_data):
            rank_item = QTableWidgetItem(str(i + 1))
            rank_item.setTextAlignment(Qt.AlignCenter)

            time_item = QTableWidgetItem(f"{record['time']:.2f}")
            time_item.setTextAlignment(Qt.AlignCenter)

            steps_item = QTableWidgetItem(str(record["steps"]))
            steps_item.setTextAlignment(Qt.AlignCenter)

            date_item = QTableWidgetItem(record["date"])
            date_item.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(i, 0, rank_item)
            self.table.setItem(i, 1, time_item)
            self.table.setItem(i, 2, steps_item)
            self.table.setItem(i, 3, date_item)

        self.table.resizeColumnsToContents()