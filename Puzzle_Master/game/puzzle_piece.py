from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt


class PuzzlePiece(QLabel):
    """拼图块组件"""
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