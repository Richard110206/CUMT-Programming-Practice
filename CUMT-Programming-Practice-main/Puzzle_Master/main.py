#!/usr/bin/env python3
"""
拼图游戏主程序
趣味拼图游戏 - 支持休闲模式和挑战模式
"""

import sys
import random
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QFileDialog, QLabel, QPushButton, QGridLayout, QMessageBox,
                             QDialog)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QBrush
from PyQt5.QtCore import Qt, QTimer, QDate
import json

# 导入模块组件
from game.puzzle_piece import PuzzlePiece
from game.game_logic import GameLogic
from ui.leaderboard_window import LeaderboardWindow


class DifficultySelectionWindow(QDialog):
    """难度选择窗口 - 修复显示问题版本"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("选择难度")
        self.setFixedSize(500, 450)
        self.setModal(True)
        self.selected_difficulty = None
        self.init_ui()

    def init_ui(self):
        # 设置窗口
        self.setStyleSheet("background-color: #4CAF50;")
        self.setFixedSize(450, 350)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # 标题
        title_label = QLabel("选择游戏难度")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                background-color: rgba(0, 0, 0, 120);
                padding: 10px;
                border-radius: 8px;
                margin-bottom: 5px;
            }
        """)
        main_layout.addWidget(title_label)

        # 难度按钮布局
        button_grid = QGridLayout()
        button_grid.setSpacing(12)
        button_grid.setContentsMargins(0, 0, 0, 0)

        # 定义四个难度档位
        difficulties = [
            {"size": 3, "name": "简单", "color": "#4CAF50", "desc": "3×3"},
            {"size": 4, "name": "普通", "color": "#FF9800", "desc": "4×4"},
            {"size": 5, "name": "困难", "color": "#F44336", "desc": "5×5"},
            {"size": 6, "name": "专家", "color": "#9C27B0", "desc": "6×6"}
        ]

        self.difficulty_buttons = []
        for i, diff in enumerate(difficulties):
            btn = QPushButton()
            btn.clicked.connect(lambda checked, size=diff['size']: self.confirm_selection(size))

            # 设置按钮文字和样式
            btn.setText(f"{diff['desc']}\n{diff['name']}")
            btn.setFont(QFont("Arial", 14, QFont.Bold))

            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {diff['color']};
                    color: white;
                    border: 3px solid white;
                    border-radius: 10px;
                    padding: 12px;
                    font-weight: bold;
                    font-size: 14px;
                    min-width: 90px;
                    min-height: 70px;
                    text-align: center;
                }}
                QPushButton:hover {{
                    background-color: {diff['color']};
                    border: 4px solid #FFD700;
                }}
                QPushButton:pressed {{
                    background-color: {diff['color']};
                    border: 2px solid white;
                }}
            """)

            # 添加到网格布局（2×2）
            button_grid.addWidget(btn, i // 2, i % 2)
            self.difficulty_buttons.append(btn)

        main_layout.addLayout(button_grid)

        # 取消按钮
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setFont(QFont("Arial", 12, QFont.Bold))
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 200);
                color: #333;
                border: 2px solid #333;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 12px;
                min-width: 80px;
                min-height: 30px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 255);
                border-color: #000;
            }
        """)

        # 居中显示取消按钮
        cancel_layout = QHBoxLayout()
        cancel_layout.addStretch()
        cancel_layout.addWidget(cancel_btn)
        cancel_layout.addStretch()

        main_layout.addLayout(cancel_layout)

    def update_suffix(self, value):
        """更新SpinBox的后缀显示"""
        self.size_input.setSuffix(f" × {value}")

    def confirm_selection(self, size=None):
        """确认选择"""
        if size is not None:
            self.selected_difficulty = size
        else:
            self.selected_difficulty = self.size_input.value()
        self.accept()

    def get_selected_difficulty(self):
        return self.selected_difficulty


class PuzzleGame(QMainWindow):
    """完整的拼图游戏实现"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("趣味拼图游戏")
        self.resize(800, 600)
        self.n = 3
        self.pieces = []
        self.original_indices = []
        self.current_indices = []
        self.selected_piece = None
        self.elapsed_time = 0
        self.step_count = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.game_mode = "休闲"
        self.timer_label = None
        self.step_label = None
        self.mode_label = None
        self.original_pixmap = None

        self.init_cover()

    def hex_to_rgb(self, hex_color):
        """十六进制颜色转RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def darken_color(self, color):
        """加深颜色"""
        if color == "#4CAF50":
            return "#45a049"
        elif color == "#F18F01":
            return "#d17a01"
        elif color == "#2E86AB":
            return "#287595"
        elif color == "#A23B72":
            return "#922e64"
        else:
            return color

    def style_button(self, button, color):
        """设置按钮样式"""
        button_font = QFont("Arial", 14, QFont.Bold)
        button.setFont(button_font)
        r, g, b = self.hex_to_rgb(color)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: none;
                color: white;
                padding: 15px 25px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                font-weight: bold;
                margin: 4px 2px;
                border-radius: 10px;
                background-color: rgba({r}, {g}, {b}, 220);
                min-width: 180px;
            }}
            QPushButton:hover {{
                background-color: rgba({r}, {g}, {b}, 240);
            }}
        """)
        button.setMinimumWidth(200)

    def init_cover(self):
        """初始化封面界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        background_path = "banner.jpg"
        if os.path.exists(background_path):
            palette = QPalette()
            pixmap = QPixmap(background_path)
            palette.setBrush(QPalette.Window, QBrush(pixmap.scaled(
                self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
            central_widget.setPalette(palette)
            central_widget.setAutoFillBackground(True)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        top_right_layout = QHBoxLayout()
        top_right_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)
        top_right_layout.setContentsMargins(620,20,20,20)

        button_container = QWidget()
        button_container.setStyleSheet("background-color: rgba(255, 255, 255, 180); border-radius: 10px; padding: 10px;")
        button_layout = QVBoxLayout(button_container)
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(15, 15, 15, 15)

        title_label = QLabel("趣味拼图游戏")
        title_font = QFont("Arial", 20, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #333; margin-bottom: 10px;")
        button_layout.addWidget(title_label)

        casual_btn = QPushButton("休闲模式")
        casual_btn.clicked.connect(lambda: self.start_game("休闲"))
        self.style_button(casual_btn, "#4CAF50")
        button_layout.addWidget(casual_btn)

        challenge_btn = QPushButton("挑战模式")
        challenge_btn.clicked.connect(lambda: self.start_game("挑战"))
        self.style_button(challenge_btn, "#F18F01")
        button_layout.addWidget(challenge_btn)

        leaderboard_btn = QPushButton("查看排行榜")
        leaderboard_btn.clicked.connect(self.show_leaderboard)
        self.style_button(leaderboard_btn, "#2E86AB")
        button_layout.addWidget(leaderboard_btn)

        quit_btn = QPushButton("退出游戏")
        quit_btn.clicked.connect(self.close)
        self.style_button(quit_btn, "#A23B72")
        button_layout.addWidget(quit_btn)

        button_container.setLayout(button_layout)
        top_right_layout.addWidget(button_container)
        top_right_layout.addStretch()

        main_layout.addLayout(top_right_layout)
        main_layout.addStretch()

    def show_leaderboard(self):
        """显示排行榜"""
        self.leaderboard_window = LeaderboardWindow(self)
        self.leaderboard_window.show()

    def start_game(self, mode):
        """开始游戏"""
        self.game_mode = mode
        if self.game_mode == "挑战":
            self.n = 4
            self.init_game_ui()
        else:
            # 使用新的难度选择窗口
            difficulty_dialog = DifficultySelectionWindow(self)
            if difficulty_dialog.exec_() == 1:  # QDialog.Accepted
                selected_difficulty = difficulty_dialog.get_selected_difficulty()
                if selected_difficulty is not None:
                    self.n = selected_difficulty
                    self.init_game_ui()

    def init_game_ui(self):
        """初始化游戏界面"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        background_path = "background.jpg"
        if os.path.exists(background_path):
            palette = QPalette()
            pixmap = QPixmap(background_path)
            scaled_pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            palette.setBrush(QPalette.Window, QBrush(scaled_pixmap))
            central_widget.setPalette(palette)
            central_widget.setAutoFillBackground(True)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        info_layout = QHBoxLayout()
        info_layout.setSpacing(30)
        info_layout.setAlignment(Qt.AlignCenter)
        info_layout.setContentsMargins(0, 0, 0, 0)

        self.mode_label = QLabel(f"模式: {self.game_mode} ({self.n}x{self.n})")
        self.timer_label = QLabel("时间: 0.00秒")
        self.step_label = QLabel("步数: 0步")

        font = QFont("Arial", 14, QFont.Bold)
        self.mode_label.setFont(font)
        self.timer_label.setFont(font)
        self.step_label.setFont(font)

        label_style = "color: white; padding: 8px 15px; background-color: rgba(0, 0, 0, 150); border-radius: 8px;"
        self.mode_label.setStyleSheet(label_style)
        self.timer_label.setStyleSheet(label_style)
        self.step_label.setStyleSheet(label_style)

        self.mode_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.step_label.setAlignment(Qt.AlignCenter)

        info_layout.addWidget(self.mode_label)
        info_layout.addWidget(self.timer_label)
        info_layout.addWidget(self.step_label)
        main_layout.addLayout(info_layout)

        self.game_area = QWidget()
        self.game_area.setStyleSheet("background-color: transparent;")
        main_layout.addWidget(self.game_area)
        main_layout.setStretchFactor(self.game_area, 1)

        self.grid_container = QWidget()
        self.grid_container.setStyleSheet("background-color: transparent; border: none;")
        self.grid_container.setVisible(False)
        grid_main_layout = QVBoxLayout(self.grid_container)
        grid_main_layout.setContentsMargins(0, 0, 0, 0)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)

        grid_main_layout.addLayout(self.grid_layout)
        main_layout.addWidget(self.grid_container)

        self.complete_image_label = QLabel()
        self.complete_image_label.setAlignment(Qt.AlignCenter)
        self.complete_image_label.setVisible(False)
        main_layout.addWidget(self.complete_image_label)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setAlignment(Qt.AlignCenter)

        self.select_btn = QPushButton("选择图片")
        self.select_btn.clicked.connect(self.select_image)
        self.reset_btn = QPushButton("重置游戏")
        self.reset_btn.clicked.connect(self.reset_puzzle)
        self.reset_btn.setEnabled(False)

        self.back_btn = QPushButton("返回首页")
        self.back_btn.clicked.connect(self.init_cover)

        btn_font = QFont("Arial", 12, QFont.Bold)
        self.select_btn.setFont(btn_font)
        self.reset_btn.setFont(btn_font)
        self.back_btn.setFont(btn_font)

        button_style = """
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 12px 24px;
                text-align: center;
                text-decoration: none;
                font-size: 12px;
                font-weight: bold;
                margin: 4px 2px;
                border-radius: 8px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """
        self.select_btn.setStyleSheet(button_style)
        self.reset_btn.setStyleSheet(button_style)
        self.back_btn.setStyleSheet(button_style.replace("#4CAF50", "#2196F3").replace("#45a049", "#1976D2"))

        btn_layout.addWidget(self.select_btn)
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addWidget(self.back_btn)
        main_layout.addLayout(btn_layout)

    def select_image(self):
        """选择图片"""
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.png *.jpg *.jpeg)")
        if not file_path:
            return

        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            QMessageBox.warning(self, "错误", "无法加载图片，请选择有效的图片文件。")
            return

        self.original_pixmap = pixmap.copy()

        target_size = 600
        pixmap = pixmap.scaled(target_size, target_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        width = pixmap.width() // self.n
        height = pixmap.height() // self.n

        self.clear_puzzle_layout()

        self.pieces.clear()
        self.original_indices.clear()
        self.current_indices.clear()

        for i in range(self.n):
            for j in range(self.n):
                x = j * width
                y = i * height

                w = width if j < self.n - 1 else pixmap.width() - x
                h = height if i < self.n - 1 else pixmap.height() - y

                piece_pixmap = pixmap.copy(x, y, w, h)
                index = i * self.n + j
                piece = PuzzlePiece(piece_pixmap, index)
                piece.main_window = self
                self.pieces.append(piece)
                self.original_indices.append(index)
                self.current_indices.append(index)

        self.shuffle_pieces()
        self.reset_btn.setEnabled(True)

        self.grid_container.setVisible(True)
        self.complete_image_label.setVisible(False)

        self.reset_timer_and_steps()

    def clear_puzzle_layout(self):
        """清空拼图布局"""
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

    def display_pieces(self):
        """显示拼图块"""
        self.clear_puzzle_layout()
        for i in range(self.n):
            for j in range(self.n):
                idx = i * self.n + j
                try:
                    piece_index = self.current_indices.index(idx)
                    piece = self.pieces[piece_index]
                    self.grid_layout.addWidget(piece, i, j)
                    piece.setContentsMargins(0, 0, 0, 0)
                    piece.setMinimumSize(0, 0)
                    piece.setMaximumSize(16777215, 16777215)
                except ValueError:
                    placeholder = QLabel()
                    placeholder.setFixedSize(100, 100)
                    placeholder.setStyleSheet("background-color: gray;")
                    self.grid_layout.addWidget(placeholder, i, j)

        self.grid_layout.setSpacing(0)
        self.grid_layout.setAlignment(Qt.AlignCenter)

    def shuffle_pieces(self):
        """打乱拼图块"""
        shuffled_indices = self.original_indices.copy()
        random.shuffle(shuffled_indices)

        for i, piece in enumerate(self.pieces):
            piece.index = shuffled_indices[i]
            self.current_indices[i] = shuffled_indices[i]

        self.display_pieces()

    def piece_clicked(self, piece):
        """处理拼图块点击"""
        if self.selected_piece == piece:
            self.selected_piece.set_selected(False)
            self.selected_piece = None
            return

        if self.selected_piece is None:
            self.selected_piece = piece
            piece.set_selected(True)
        else:
            self.exchange_pieces(self.selected_piece.index, piece.index)
            self.selected_piece.set_selected(False)
            self.selected_piece = None

    def exchange_pieces(self, source_index, target_index):
        """交换两个拼图块"""
        self.step_count += 1
        self.update_step_display()

        GameLogic.exchange_pieces(self.pieces, self.current_indices, source_index, target_index)
        self.display_pieces()

        if GameLogic.is_puzzle_complete(self.current_indices, self.original_indices):
            self.timer.stop()

            if self.game_mode == "挑战":
                GameLogic.save_to_leaderboard(self.elapsed_time, self.step_count)

            self.show_complete_image()

            QMessageBox.information(self, "恭喜",
                f"拼图完成！\n用时: {self.elapsed_time:.2f}秒\n步数: {self.step_count}步")

    def show_complete_image(self):
        """显示完整图片"""
        if self.original_pixmap:
            self.grid_container.setVisible(False)

            scaled_pixmap = self.original_pixmap.scaled(
                self.game_area.size() * 1.2,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.complete_image_label.setPixmap(scaled_pixmap)
            self.complete_image_label.setVisible(True)

    def reset_timer_and_steps(self):
        """重置计时器和步数"""
        self.timer.stop()
        self.elapsed_time = 0
        self.step_count = 0
        self.update_timer_display()
        self.update_step_display()
        self.timer.start(100)

    def update_timer(self):
        """更新计时器"""
        self.elapsed_time += 0.1
        self.update_timer_display()

    def update_timer_display(self):
        """更新时间显示"""
        self.timer_label.setText(f"时间: {self.elapsed_time:.2f}秒")

    def update_step_display(self):
        """更新步数显示"""
        self.step_label.setText(f"步数: {self.step_count}步")

    def reset_puzzle(self):
        """重置拼图"""
        self.complete_image_label.setVisible(False)
        self.grid_container.setVisible(True)
        self.shuffle_pieces()
        self.reset_timer_and_steps()


def main():
    """主函数"""
    app = QApplication(sys.argv)

    # 设置应用程序信息
    app.setApplicationName("趣味拼图游戏")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("PuzzleMaster")

    # 创建并显示主窗口
    puzzle_game = PuzzleGame()
    puzzle_game.show()

    # 运行应用程序
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()