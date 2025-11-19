import sys
import random
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, 
                             QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
                             QWidget, QInputDialog, QMessageBox, QTableWidget, QTableWidgetItem,
                             QGridLayout)
from PyQt5.QtGui import QPixmap, QFont, QPalette, QBrush
from PyQt5.QtCore import Qt, QTimer, QDate


class PuzzlePiece(QLabel):
    def __init__(self, pixmap, index, parent=None):
        super().__init__(parent)
        self.setPixmap(pixmap)
        self.index = index  
        self.original_index = index  
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            border: none; 
            margin: -1px; 
            padding: 0px;
        """)
        
        # 保存对主窗口的引用
        self.main_window = None
        
        # 标记是否被选中
        self.is_selected = False

    def mousePressEvent(self, event):
        """鼠标按下时，处理点击事件"""
        if event.button() == Qt.LeftButton:
            # 通知主窗口处理点击事件
            if self.main_window:
                self.main_window.piece_clicked(self)
        
    def set_selected(self, selected):
        """设置选中状态的视觉反馈"""
        self.is_selected = selected
        if selected:
            # 选中时添加边框效果，使用负边距补偿
            self.setStyleSheet("""
                border: 3px solid red; 
                margin: -4px; 
                padding: 0px;
            """)
        else:
            # 取消选中时移除边框，恢复负边距
            self.setStyleSheet("""
                border: none; 
                margin: -1px; 
                padding: 0px;
            """)


class LeaderboardWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("排行榜")
        self.resize(500, 400)
        self.load_leaderboard()
        self.init_ui()

    def init_ui(self):
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
        main_layout.setContentsMargins(20, 20, 20, 20) 
        main_layout.setSpacing(15) 
        
        title_label = QLabel("挑战模式排行榜")
        title_font = QFont("Arial", 18, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: white; background-color: rgba(0, 0, 0, 120); padding: 10px; border-radius: 10px;")
        main_layout.addWidget(title_label)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["排名", "时间(秒)", "步数", "日期"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers) 
        self.table.setSelectionBehavior(QTableWidget.SelectRows)  
        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.setStyleSheet("""
QTableWidget {
            background-color: rgba(255, 255, 255, 200);
                border: 2px solid #4CAF50;
                border-radius: 8px;
                gridline-color: #ddd;
            }
            QHeaderView::section {
            background-color: #4CAF50;
                color: white;
                padding: 4px;
                font-weight: bold;
                border: 1px solid #45a049;
            }
        """)
        main_layout.addWidget(self.table)

        self.populate_table()

        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 12px 24px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                font-weight: bold;
                margin: 4px 2px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

    def load_leaderboard(self):
        self.leaderboard_data = []
        if os.path.exists("leaderboard.json"):
            try:
                with open("leaderboard.json", "r", encoding="utf-8") as f:
                    self.leaderboard_data = json.load(f)
                self.leaderboard_data.sort(key=lambda x: x["time"])
            except:
                self.leaderboard_data = []

    def populate_table(self):
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


class PuzzleGame(QMainWindow):
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

    def init_cover(self):
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

        # 退出按钮
        quit_btn = QPushButton("退出游戏")
        quit_btn.clicked.connect(self.close)
        self.style_button(quit_btn, "#A23B72")
        button_layout.addWidget(quit_btn)

        button_container.setLayout(button_layout)
        top_right_layout.addWidget(button_container)
        top_right_layout.addStretch()  # 添加弹性空间

        main_layout.addLayout(top_right_layout)
        main_layout.addStretch() 

    def style_button(self, button, color):
        button_font = QFont("Arial", 14, QFont.Bold)
        button.setFont(button_font)
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
                background-color: rgba({self.hex_to_rgb(color)[0]}, {self.hex_to_rgb(color)[1]}, {self.hex_to_rgb(color)[2]}, 220);
                min-width: 180px;
            }}
            QPushButton:hover {{
                background-color: rgba({self.hex_to_rgb(self.darken_color(color))[0]}, {self.hex_to_rgb(self.darken_color(color))[1]}, {self.hex_to_rgb(self.darken_color(color))[2]}, 240);
                transform: scale(1.05);
            }}
        """)
        button.setMinimumWidth(200)

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def darken_color(self, color):
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

    def show_leaderboard(self):
        self.leaderboard_window = LeaderboardWindow(self)
        self.leaderboard_window.show()
    def start_game(self, mode):
        self.game_mode = mode
        if self.game_mode == "挑战":
            self.n = 4  
        else:
            difficulty, ok = QInputDialog.getInt(self, "选择难度", "请输入拼图的行列数（例如：3表示3×3）:", 
                                               value=3, min=2, max=6)
            if not ok:
                return
            self.n = difficulty
        self.init_game_ui()

    def display_pieces(self):
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

    def init_game_ui(self):
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
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

    def shuffle_pieces(self):
        shuffled_indices = self.original_indices.copy()
        random.shuffle(shuffled_indices)

        for i, piece in enumerate(self.pieces):
            piece.index = shuffled_indices[i]
            self.current_indices[i] = shuffled_indices[i]

        self.display_pieces()

    def piece_clicked(self, piece):
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
        self.step_count += 1
        self.update_step_display()
        
        source_pos = self.current_indices.index(source_index)
        target_pos = self.current_indices.index(target_index)

        self.current_indices[source_pos], self.current_indices[target_pos] = \
            self.current_indices[target_pos], self.current_indices[source_pos]
        
        self.pieces[source_pos].index = self.current_indices[source_pos]
        self.pieces[target_pos].index = self.current_indices[target_pos]
        
        self.display_pieces()
        
        if self.current_indices == self.original_indices:
            self.timer.stop()

            if self.game_mode == "挑战":
                self.save_to_leaderboard()

            self.show_complete_image()

            QMessageBox.information(self, "恭喜", f"拼图完成！\n用时: {self.elapsed_time:.2f}秒\n步数: {self.step_count}步")

    def show_complete_image(self):
        if self.original_pixmap:
            self.grid_container.setVisible(False)
            
            scaled_pixmap = self.original_pixmap.scaled(
                self.game_area.size() * 1.2,  
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.complete_image_label.setPixmap(scaled_pixmap)
            self.complete_image_label.setVisible(True)

    def save_to_leaderboard(self):
        record = {
            "time": self.elapsed_time,
            "steps": self.step_count,
            "date": QDate.currentDate().toString("yyyy-MM-dd")
        }
        
        leaderboard_data = []
        if os.path.exists("leaderboard.json"):
            try:
                with open("leaderboard.json", "r", encoding="utf-8") as f:
                    leaderboard_data = json.load(f)
            except:
                pass
        
        leaderboard_data.append(record)

        try:
            with open("leaderboard.json", "w", encoding="utf-8") as f:
                json.dump(leaderboard_data, f, ensure_ascii=False, indent=2)
        except:
            pass

    def reset_timer_and_steps(self):
        self.timer.stop()
        self.elapsed_time = 0
        self.step_count = 0
        self.update_timer_display()
        self.update_step_display()
        self.timer.start(100) 

    def update_timer(self):
        self.elapsed_time += 0.1
        self.update_timer_display()

    def update_timer_display(self):
        self.timer_label.setText(f"时间: {self.elapsed_time:.2f}秒")

    def update_step_display(self):
        self.step_label.setText(f"步数: {self.step_count}步")

    def reset_puzzle(self):
        self.complete_image_label.setVisible(False)
        self.grid_container.setVisible(True)
        self.shuffle_pieces()
        self.reset_timer_and_steps()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    puzzle_game = PuzzleGame()
    puzzle_game.show()
    sys.exit(app.exec_())