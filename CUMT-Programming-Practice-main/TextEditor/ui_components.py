#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI组件模块
定义复用的UI组件
"""

from PyQt5.QtWidgets import (QToolBar, QFontComboBox, QComboBox, QPushButton, QLabel,
                           QColorDialog, QHBoxLayout, QVBoxLayout, QWidget, QComboBox, QSizePolicy)
from PyQt5.QtCore import Qt
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
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # 设置按钮样式
        button_style = "font-size: 14px; padding: 8px 12px;"
        
        # 添加字体选择框
        font_label = QLabel("字体:", self)
        font_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(font_label)
        
        self.font_combo = QFontComboBox(self)
        self.font_combo.setStyleSheet("font-size: 14px; padding: 3px; min-width: 10px;")
        self.font_combo.setSizeAdjustPolicy(QComboBox.AdjustToContentsOnFirstShow)
        self.font_combo.setMinimumHeight(40)
        
        # 添加中文字体
        self.font_combo.addItems(["SimSun", "SimHei"])
        layout.addWidget(self.font_combo)
        
        # 添加字号选择框
        size_label = QLabel("字号:", self)
        size_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(size_label)
        
        self.size_combo = QComboBox(self)
        self.size_combo.setStyleSheet("font-size: 16px; padding: 12px; min-width: 60px;")
        # 添加常用字号
        for size in range(8, 73, 2):
            self.size_combo.addItem(str(size))
        # 默认选择20号字体
        self.size_combo.setCurrentText("24")
        layout.addWidget(self.size_combo)
        
        # 添加颜色按钮
        self.color_button = QPushButton("颜色", self)
        self.color_button.setStyleSheet(button_style)
        layout.addWidget(self.color_button)
        
        # 添加粗体按钮
        self.bold_button = QPushButton("粗体", self)
        self.bold_button.setStyleSheet(button_style)
        self.bold_button.setCheckable(True)  # 设置为可切换状态
        layout.addWidget(self.bold_button)
        
        # 添加斜体按钮
        self.italic_button = QPushButton("斜体", self)
        self.italic_button.setStyleSheet(button_style)
        self.italic_button.setCheckable(True)  # 设置为可切换状态
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
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # 设置样式
        label_style = "font-size: 16px;"
        combo_style = "font-size: 18px; padding: 8px; min-width: 100px;"
        
        # 添加首行缩进选项
        indent_label = QLabel("首行缩进:", self)
        indent_label.setStyleSheet(label_style)
        layout.addWidget(indent_label)
        
        self.indent_combo = QComboBox(self)
        self.indent_combo.setStyleSheet(combo_style)
        self.indent_combo.addItems(["无缩进", "2字符", "4字符"])
        self.indent_combo.setCurrentText("无缩进")
        layout.addWidget(self.indent_combo)
        
        # 添加段落间距选项
        spacing_label = QLabel("段落间距:", self)
        spacing_label.setStyleSheet(label_style)
        layout.addWidget(spacing_label)
        
        self.spacing_combo = QComboBox(self)
        self.spacing_combo.setStyleSheet(combo_style)
        self.spacing_combo.addItems(["单倍", "1.5倍", "双倍"])
        self.spacing_combo.setCurrentText("单倍")
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
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # 设置按钮样式
        button_style = "font-size: 16px; padding: 8px 12px;"
        
        # 添加对齐按钮
        self.left_align_button = QPushButton("左对齐", self)
        self.left_align_button.setStyleSheet(button_style)
        layout.addWidget(self.left_align_button)
        
        self.center_align_button = QPushButton("居中对齐", self)
        self.center_align_button.setStyleSheet(button_style)
        layout.addWidget(self.center_align_button)
        
        self.right_align_button = QPushButton("右对齐", self)
        self.right_align_button.setStyleSheet(button_style)
        layout.addWidget(self.right_align_button)
    
    def connect_signals(self, left_align_handler, center_align_handler, right_align_handler):
        """
        连接信号和槽函数
        :param left_align_handler: 左对齐的处理函数
        :param center_align_handler: 居中对齐的处理函数
        :param right_align_handler: 右对齐的处理函数
        """
        self.left_align_button.clicked.connect(left_align_handler)
        self.center_align_button.clicked.connect(center_align_handler)
        self.right_align_button.clicked.connect(right_align_handler)


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
        初始化DeepSeek功能控制面板
        """
        layout = QVBoxLayout(self)  # 改为垂直布局
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(8)
        
        # 设置样式
        label_style = "font-size: 22px; font-weight: bold; color: #283593; qproperty-alignment: AlignCenter;"
        combo_style = "font-size: 16px; padding: 8px; min-width: 140px; border: 1px solid #90CAF9; border-radius: 4px;"
        button_style = "font-size: 16px; padding: 8px 12px; font-weight: bold; background-color: #1976D2; color: white; border-radius: 4px; border: none;"
        
        # 添加标签
        label = QLabel("DeepSeek功能", self)
        label.setStyleSheet(label_style)
        label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        layout.addWidget(label)
        
        # 创建水平布局用于放置选择框和按钮
        h_layout = QHBoxLayout()
        h_layout.setSpacing(8)
        
        # 添加下拉选择框
        self.function_combo = QComboBox(self)
        self.function_combo.setStyleSheet(combo_style)
        self.function_combo.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.function_combo.addItems(["文本续写", "文本总结"])
        h_layout.addWidget(self.function_combo)
        
        # 添加触发按钮
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
        super().__init__("工具栏", parent)
        self.font_panel = None
        self.format_panel = None
        self.mode_panel = None
        self.alignment_panel = None
        self.init_ui()
    
    def init_ui(self):
        """
        初始化主工具栏
        """
        # 创建并添加字体控制面板
        self.font_panel = FontControlPanel(self)
        self.addWidget(self.font_panel)
        
        # 添加分隔线
        self.addSeparator()
        
        # 创建并添加格式控制面板
        self.format_panel = FormatControlPanel(self)
        self.addWidget(self.format_panel)
        
        # 添加分隔线
        self.addSeparator()
        
        # 创建并添加对齐控制面板
        self.alignment_panel = AlignmentControlPanel(self)
        self.addWidget(self.alignment_panel)
    
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