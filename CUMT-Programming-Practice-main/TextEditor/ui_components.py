#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI组件模块
定义复用的UI组件
"""

from PyQt5.QtWidgets import (
    QToolBar,
    QFontComboBox,
    QComboBox,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
    QTextEdit,
)
from PyQt5.QtCore import Qt


class FontControlPanel(QWidget):
    """
    字体控制面板组件
    包含字体选择、字号选择、颜色设置等功能
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """
        初始化字体控制面板
        """
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(8)

        # 设置现代化样式
        button_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2196F3, stop:1 #1976D2);
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
                padding: 8px 16px;
                min-width: 60px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #42A5F5, stop:1 #2196F3);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #1976D2, stop:1 #1565C0);
            }
            QPushButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4CAF50, stop:1 #388E3C);
            }
        """

        toggle_button_style = """
            QPushButton {
                background: #f5f5f5;
                color: #333;
                border: 1px solid #ddd;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
                padding: 8px 16px;
                min-width: 60px;
            }
            QPushButton:hover {
                background: #e8eaf6;
                border-color: #2196F3;
            }
            QPushButton:pressed {
                background: #d0d0d0;
            }
            QPushButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #4CAF50, stop:1 #388E3C);
                color: white;
                border-color: #388E3C;
            }
        """

        combo_box_style = """
            QComboBox {
                background: white;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                min-height: 20px;
                color: #2d3748;
            }
            QComboBox:hover {
                border-color: #3182ce;
                background: #f7fafc;
            }
            QComboBox:focus {
                border-color: #3182ce;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #4a5568;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                selection-background-color: #ebf8ff;
                color: #2d3748;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                color: #2d3748;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #ebf8ff;
                color: #2b6cb0;
            }
        """

        label_style = """
            QLabel {
                color: #4a5568;
                font-size: 13px;
                font-weight: 600;
                padding: 0 5px;
            }
        """

        # 添加字体选择图标和标签
        font_label = QLabel("📝 字体", self)
        font_label.setStyleSheet(label_style)
        layout.addWidget(font_label)

        self.font_combo = QFontComboBox(self)
        self.font_combo.setStyleSheet(combo_box_style)
        self.font_combo.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.font_combo.setMinimumHeight(36)

        # 添加中文字体
        self.font_combo.addItems(["SimSun", "SimHei", "Microsoft YaHei"])
        layout.addWidget(self.font_combo)

        # 添加字号选择图标和标签
        size_label = QLabel("📏 字号", self)
        size_label.setStyleSheet(label_style)
        layout.addWidget(size_label)

        self.size_combo = QComboBox(self)
        self.size_combo.setStyleSheet(combo_box_style)
        self.size_combo.setMinimumWidth(80)
        self.size_combo.setMinimumHeight(36)
        # 添加常用字号
        for size in range(8, 73, 2):
            self.size_combo.addItem(str(size))
        # 默认选择24号字体
        self.size_combo.setCurrentText("24")
        layout.addWidget(self.size_combo)

        # 添加颜色按钮
        self.color_button = QPushButton("🎨 颜色", self)
        self.color_button.setStyleSheet(button_style)
        self.color_button.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.color_button)

        # 添加粗体按钮
        self.bold_button = QPushButton("B 粗体", self)
        self.bold_button.setStyleSheet(toggle_button_style)
        self.bold_button.setCheckable(True)
        self.bold_button.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.bold_button)

        # 添加斜体按钮
        self.italic_button = QPushButton("I 斜体", self)
        self.italic_button.setStyleSheet(toggle_button_style)
        self.italic_button.setCheckable(True)
        self.italic_button.setCursor(Qt.PointingHandCursor)
        layout.addWidget(self.italic_button)

    def connect_signals(self, font_changed_handler, size_changed_handler, color_clicked_handler, bold_clicked_handler=None, italic_clicked_handler=None):
        """
        连接信号和槽函数
        :param font_changed_handler: 字体改变的处理函数
        :param size_changed_handler: 字号改变的处理函数
        :param color_clicked_handler: 颜色按钮点击的处理函数
        :param bold_clicked_handler: 粗体按钮点击的处理函数
        :param italic_clicked_handler: 斜体按钮点击的处理函数
        """
        self.font_combo.currentFontChanged.connect(
            lambda font: font_changed_handler(font.family())
        )
        self.size_combo.currentTextChanged.connect(size_changed_handler)
        self.color_button.clicked.connect(color_clicked_handler)
        if bold_clicked_handler:
            self.bold_button.clicked.connect(bold_clicked_handler)
        if italic_clicked_handler:
            self.italic_button.clicked.connect(italic_clicked_handler)

    def get_current_font(self):
        """
        获取当前选择的字体
        :return: 字体名称
        """
        return self.font_combo.currentFont().family()

    def get_current_size(self):
        """
        获取当前选择的字号
        :return: 字号字符串
        """
        return self.size_combo.currentText()


class FormatControlPanel(QWidget):
    """
    格式控制面板组件
    包含首行缩进等格式设置功能
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """
        初始化格式控制面板
        """
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(8)

        # 设置现代化样式
        combo_box_style = """
            QComboBox {
                background: white;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                min-height: 20px;
                min-width: 100px;
                color: #2d3748;
            }
            QComboBox:hover {
                border-color: #3182ce;
                background: #f7fafc;
            }
            QComboBox:focus {
                border-color: #3182ce;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #4a5568;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                selection-background-color: #ebf8ff;
                color: #2d3748;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                color: #2d3748;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #ebf8ff;
                color: #2b6cb0;
            }
        """

        label_style = """
            QLabel {
                color: #4a5568;
                font-size: 13px;
                font-weight: 600;
                padding: 0 5px;
            }
        """

        # 添加首行缩进图标和选项
        indent_label = QLabel("↩️ 首行缩进", self)
        indent_label.setStyleSheet(label_style)
        layout.addWidget(indent_label)

        self.indent_combo = QComboBox(self)
        self.indent_combo.setStyleSheet(combo_box_style)
        self.indent_combo.addItems(["无缩进", "2字符", "4字符", "6字符"])
        self.indent_combo.setCurrentText("无缩进")
        self.indent_combo.setMinimumHeight(36)
        layout.addWidget(self.indent_combo)

        # 添加段落间距图标和选项
        spacing_label = QLabel("📐 段落间距", self)
        spacing_label.setStyleSheet(label_style)
        layout.addWidget(spacing_label)

        self.spacing_combo = QComboBox(self)
        self.spacing_combo.setStyleSheet(combo_box_style)
        self.spacing_combo.addItems(["单倍", "1.5倍", "双倍", "2.5倍"])
        self.spacing_combo.setCurrentText("单倍")
        self.spacing_combo.setMinimumHeight(36)
        layout.addWidget(self.spacing_combo)




class AlignmentControlPanel(QWidget):
    """
    对齐方式控制面板
    包含左对齐、居中对齐、右对齐按钮
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """
        初始化对齐方式控制面板
        """
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(8)

        # 设置现代化按钮样式
        button_style = """
            QPushButton {
                background: #f8f9fa;
                color: #2d3748;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 500;
                padding: 8px 16px;
                min-width: 70px;
                text-align: left;
            }
            QPushButton:hover {
                background: #ebf8ff;
                border-color: #3182ce;
                color: #2b6cb0;
            }
            QPushButton:pressed {
                background: #bee3f8;
            }
            QPushButton:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3182ce, stop:1 #2b6cb0);
                color: white;
                border-color: #2b6cb0;
            }
        """

        label_style = """
            QLabel {
                color: #4a5568;
                font-size: 13px;
                font-weight: 600;
                padding: 0 5px;
            }
        """

        # 添加对齐图标和标签
        align_label = QLabel("⚖️ 对齐方式", self)
        align_label.setStyleSheet(label_style)
        layout.addWidget(align_label)

        # 添加对齐按钮
        self.left_align_button = QPushButton("居左", self)
        self.left_align_button.setStyleSheet(button_style)
        self.left_align_button.setCursor(Qt.PointingHandCursor)
        self.left_align_button.setCheckable(True)
        self.left_align_button.setChecked(True)
        layout.addWidget(self.left_align_button)

        self.center_align_button = QPushButton("居中", self)
        self.center_align_button.setStyleSheet(button_style)
        self.center_align_button.setCursor(Qt.PointingHandCursor)
        self.center_align_button.setCheckable(True)
        layout.addWidget(self.center_align_button)

        self.right_align_button = QPushButton("居右", self)
        self.right_align_button.setStyleSheet(button_style)
        self.right_align_button.setCursor(Qt.PointingHandCursor)
        self.right_align_button.setCheckable(True)
        layout.addWidget(self.right_align_button)

    def connect_signals(self, left_align_handler, center_align_handler, right_align_handler):
        """
        连接信号和槽函数
        :param left_align_handler: 左对齐的处理函数
        :param center_align_handler: 居中对齐的处理函数
        :param right_align_handler: 右对齐的处理函数
        """
        # 创建互斥的对齐按钮组
        self.left_align_button.clicked.connect(lambda: self._handle_alignment_click(self.left_align_button, left_align_handler))
        self.center_align_button.clicked.connect(lambda: self._handle_alignment_click(self.center_align_button, center_align_handler))
        self.right_align_button.clicked.connect(lambda: self._handle_alignment_click(self.right_align_button, right_align_handler))

    def _handle_alignment_click(self, clicked_button, handler):
        """
        处理对齐按钮点击，确保互斥选择
        :param clicked_button: 被点击的按钮
        :param handler: 对应的处理函数
        """
        # 设置所有按钮为未选中状态
        self.left_align_button.blockSignals(True)
        self.center_align_button.blockSignals(True)
        self.right_align_button.blockSignals(True)

        self.left_align_button.setChecked(False)
        self.center_align_button.setChecked(False)
        self.right_align_button.setChecked(False)

        # 设置被点击的按钮为选中状态
        clicked_button.setChecked(True)

        # 恢复信号
        self.left_align_button.blockSignals(False)
        self.center_align_button.blockSignals(False)
        self.right_align_button.blockSignals(False)

        # 调用处理函数
        handler()


class DeepSeekControlPanel(QWidget):
    """
    DeepSeek功能控制面板
    包含功能选择下拉框和执行按钮
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """
        初始化DeepSeek功能控制面板 - 精简版本
        """
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)

        # 紧凑的现代化样式
        combo_box_style = """
            QComboBox {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 13px;
                min-height: 18px;
                min-width: 120px;
                color: #2d3748;
            }
            QComboBox:hover {
                border-color: #3182ce;
                background: #f7fafc;
            }
            QComboBox:focus {
                border-color: #3182ce;
                outline: none;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
                background: transparent;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 3px solid transparent;
                border-right: 3px solid transparent;
                border-top: 3px solid #4a5568;
                margin-right: 4px;
            }
            QComboBox QAbstractItemView {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                selection-background-color: #ebf8ff;
                selection-color: #2b6cb0;
                color: #2d3748;
            }
            QComboBox QAbstractItemView::item {
                padding: 4px 8px;
                color: #2d3748;
            }
        """

        button_style = """
            QPushButton {
                background: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 11px;
                font-weight: 600;
                padding: 4px 12px;
                min-width: 50px;
                min-height: 16px;
            }
            QPushButton:hover {
                background: #42A5F5;
            }
            QPushButton:pressed {
                background: #1976D2;
            }
        """

        # 创建紧凑的水平布局
        h_layout = QHBoxLayout()
        h_layout.setSpacing(6)
        h_layout.setContentsMargins(0, 0, 0, 0)

        # 添加精简的下拉选择框
        self.function_combo = QComboBox(self)
        self.function_combo.setStyleSheet(combo_box_style)
        self.function_combo.addItems(["文本续写", "文本总结", "智能分析", "内容优化"])
        h_layout.addWidget(self.function_combo)

        # 添加精简的执行按钮
        self.execute_button = QPushButton("执行", self)
        self.execute_button.setStyleSheet(button_style)
        self.execute_button.setCursor(Qt.PointingHandCursor)
        h_layout.addWidget(self.execute_button)

        # 将水平布局添加到主布局
        layout.addLayout(h_layout)

    def connect_signals(self, execute_handler):
        """
        连接执行按钮的信号
        :param execute_handler: 执行按钮点击的处理函数
        """
        self.execute_button.clicked.connect(execute_handler)

    def get_selected_function(self):
        """
        获取当前选择的功能
        :return: 功能名称
        """
        return self.function_combo.currentText()

    def add_function_option(self, option_text):
        """
        添加功能选项
        :param option_text: 选项文本
        """
        self.function_combo.addItem(option_text)


class MainToolBar(QToolBar):
    """
    主工具栏
    整合字体控制和对齐控制
    """
    def __init__(self, parent=None):
        super().__init__("📝 文本编辑工具栏", parent)
        self.font_panel = None
        self.format_panel = None
        self.mode_panel = None
        self.alignment_panel = None
        self.init_ui()

    def init_ui(self):
        """
        初始化主工具栏
        """
        # 设置工具栏整体样式
        self.setStyleSheet("""
            QToolBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: none;
                border-bottom: 2px solid #dee2e6;
                spacing: 6px;
                padding: 4px 8px;
            }
            QToolBar::separator {
                background: #ced4da;
                width: 1px;
                margin: 4px 2px;
            }
        """)

        # 创建容器widget用于更好的布局控制
        container = QWidget(self)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(4)

        # 第一行：字体控制
        self.font_panel = FontControlPanel(container)
        self.font_panel.setStyleSheet("""
            FontControlPanel {
                background: white;
                border-radius: 8px;
                border: 1px solid #dee2e6;
                margin: 2px;
            }
            FontControlPanel:hover {
                border-color: #2196F3;
                box-shadow: 0 0 0 1px rgba(33, 150, 243, 0.1);
            }
        """)
        container_layout.addWidget(self.font_panel)

        # 第二行：格式和对齐控制
        row2_widget = QWidget(container)
        row2_layout = QHBoxLayout(row2_widget)
        row2_layout.setContentsMargins(0, 0, 0, 0)
        row2_layout.setSpacing(8)

        # 创建并添加格式控制面板
        self.format_panel = FormatControlPanel(row2_widget)
        self.format_panel.setStyleSheet("""
            FormatControlPanel {
                background: white;
                border-radius: 8px;
                border: 1px solid #dee2e6;
                margin: 2px;
            }
            FormatControlPanel:hover {
                border-color: #2196F3;
                box-shadow: 0 0 0 1px rgba(33, 150, 243, 0.1);
            }
        """)
        row2_layout.addWidget(self.format_panel)

        # 添加分隔线
        separator = QLabel("│", row2_widget)
        separator.setStyleSheet("""
            QLabel {
                color: #ced4da;
                font-size: 16px;
                font-weight: bold;
                padding: 0 8px;
            }
        """)
        row2_layout.addWidget(separator)

        # 创建并添加对齐控制面板
        self.alignment_panel = AlignmentControlPanel(row2_widget)
        self.alignment_panel.setStyleSheet("""
            AlignmentControlPanel {
                background: white;
                border-radius: 8px;
                border: 1px solid #dee2e6;
                margin: 2px;
            }
            AlignmentControlPanel:hover {
                border-color: #2196F3;
                box-shadow: 0 0 0 1px rgba(33, 150, 243, 0.1);
            }
        """)
        row2_layout.addWidget(self.alignment_panel)

        row2_layout.addStretch()
        container_layout.addWidget(row2_widget)

        # 将容器添加到工具栏
        self.addWidget(container)

        # 设置工具栏属性
        self.setMovable(False)
        self.setFloatable(False)
        # 注释掉可能引起问题的setIconSize调用
        # self.setIconSize(None)

    def connect_font_signals(self, font_changed_handler, size_changed_handler, color_clicked_handler, bold_clicked_handler=None, italic_clicked_handler=None):
        """
        连接字体控制相关信号
        """
        if self.font_panel:
            self.font_panel.connect_signals(
                font_changed_handler,
                size_changed_handler,
                color_clicked_handler,
                bold_clicked_handler,
                italic_clicked_handler
            )

    def connect_format_signals(self, indent_changed_handler, spacing_changed_handler):
        """
        连接格式控制相关信号
        """
        if self.format_panel:
            self.format_panel.indent_combo.currentTextChanged.connect(indent_changed_handler)
            self.format_panel.spacing_combo.currentTextChanged.connect(spacing_changed_handler)

    def connect_alignment_signals(self, left_align_handler, center_align_handler, right_align_handler):
        """
        连接对齐控制相关信号
        """
        if self.alignment_panel:
            self.alignment_panel.connect_signals(
                left_align_handler,
                center_align_handler,
                right_align_handler
            )


class AIResultPanel(QWidget):
    """
    AI结果展示面板
    包含标题、操作按钮和readonly文本区域
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.text_edit = None
        self.copy_button = None
        self.clear_button = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)

        # 紧凑的头部样式
        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)
        header_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel("AI 结果", self)
        title_label.setStyleSheet("""
            QLabel {
                color: #2b6cb0;
                font-size: 16px;
                font-weight: 600;
                padding: 6px 12px;
                background: rgba(49, 130, 206, 0.08);
                border-radius: 4px;
                border-left: 3px solid #3182ce;
            }
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)

        # 增大字体按钮样式
        button_style = """
            QPushButton {
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 13px;
                font-weight: 600;
                padding: 5px 12px;
                min-width: 50px;
                min-height: 24px;
            }
        """

        self.copy_button = QPushButton("复制", self)
        self.copy_button.setCursor(Qt.PointingHandCursor)
        self.copy_button.setStyleSheet(button_style + "QPushButton { background: #2196F3; } QPushButton:hover { background: #42A5F5; }")
        header_layout.addWidget(self.copy_button)

        self.clear_button = QPushButton("清空", self)
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.setStyleSheet(button_style + "QPushButton { background: #F44336; } QPushButton:hover { background: #EF5350; }")
        header_layout.addWidget(self.clear_button)

        layout.addLayout(header_layout)

        # 增大字体的文本编辑器样式
        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)
        self.text_edit.setPlaceholderText("AI生成内容将在这里显示...")
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background: #f7fafc;
                border: 1px solid #e2e8f0;
                border-radius: 4px;
                padding: 10px;
                font-size: 17px;
                line-height: 1.6;
                color: #2d3748;
                selection-background-color: #bee3f8;
            }
            QTextEdit:focus {
                border-color: #3182ce;
                background: white;
            }
        """)
        layout.addWidget(self.text_edit)

    def connect_control_signals(self, copy_handler, clear_handler):
        self.copy_button.clicked.connect(copy_handler)
        self.clear_button.clicked.connect(clear_handler)

    def set_text(self, text):
        self.text_edit.setPlainText(text)

    def get_text(self):
        return self.text_edit.toPlainText()

    def clear_text(self):
        self.text_edit.clear()

    def apply_theme(self, theme):
        if theme == "dark":
            self.setStyleSheet("background-color: #2b2b2b; color: #ffffff;")
            self.text_edit.setStyleSheet(
                "background-color: #1f1f1f; color: #f5f5f5; border: 1px solid #444;"
            )
        else:
            self.setStyleSheet("background-color: #ffffff; color: #000000;")
            self.text_edit.setStyleSheet(
                "background-color: #fdfdfd; color: #1a1a1a; border: 1px solid #dcdcdc;"
            )

    def connect_format_signals(self, indent_changed_handler, spacing_changed_handler):
        """
        连接格式控制相关信号
        """
        if self.format_panel:
            self.format_panel.indent_combo.currentTextChanged.connect(indent_changed_handler)
            self.format_panel.spacing_combo.currentTextChanged.connect(spacing_changed_handler)

    def connect_mode_signals(self, mode_changed_handler):
        """
        连接模式控制相关信号
        """
        # 模式控制面板已被移除，此方法为空
        pass

    def connect_alignment_signals(self, left_align_handler, center_align_handler, right_align_handler):
        """
        连接对齐控制相关信号
        """
        if self.alignment_panel:
            self.alignment_panel.connect_signals(
                left_align_handler,
                center_align_handler,
                right_align_handler
            )