#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI组件模块
定义复用的UI组件
"""

from PyQt5.QtWidgets import (QToolBar, QFontComboBox, QComboBox, QPushButton, QLabel,
                           QColorDialog, QHBoxLayout, QWidget, QComboBox)
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
        layout.setSpacing(5)
        
        # 添加字体选择框
        font_label = QLabel("字体:", self)
        layout.addWidget(font_label)
        
        self.font_combo = QFontComboBox(self)
        layout.addWidget(self.font_combo)
        
        # 添加字号选择框
        size_label = QLabel("字号:", self)
        layout.addWidget(size_label)
        
        self.size_combo = QComboBox(self)
        # 添加常用字号
        for size in range(8, 73, 2):
            self.size_combo.addItem(str(size))
        # 默认选择12号字体
        self.size_combo.setCurrentText("12")
        layout.addWidget(self.size_combo)
        
        # 添加颜色按钮
        self.color_button = QPushButton("颜色", self)
        layout.addWidget(self.color_button)
        
        # 添加斜体按钮
        self.italic_button = QPushButton("斜体", self)
        layout.addWidget(self.italic_button)
        
    def connect_signals(self, font_changed_handler, size_changed_handler, color_clicked_handler, italic_clicked_handler=None):
        """
        连接信号和槽函数
        :param font_changed_handler: 字体改变的处理函数
        :param size_changed_handler: 字号改变的处理函数
        :param color_clicked_handler: 颜色按钮点击的处理函数
        :param italic_clicked_handler: 斜体按钮点击的处理函数
        """
        self.font_combo.currentFontChanged.connect(
            lambda font: font_changed_handler(font.family())
        )
        self.size_combo.currentTextChanged.connect(size_changed_handler)
        self.color_button.clicked.connect(color_clicked_handler)
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
        layout.setSpacing(5)
        
        # 添加对齐按钮
        self.left_align_button = QPushButton("左对齐", self)
        layout.addWidget(self.left_align_button)
        
        self.center_align_button = QPushButton("居中对齐", self)
        layout.addWidget(self.center_align_button)
        
        self.right_align_button = QPushButton("右对齐", self)
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
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # 添加标签
        label = QLabel("DeepSeek功能:", self)
        layout.addWidget(label)
        
        # 添加下拉选择框
        self.function_combo = QComboBox(self)
        self.function_combo.addItems(["文本续写", "文本总结"])
        layout.addWidget(self.function_combo)
        
        # 添加触发按钮
        self.execute_button = QPushButton("执行", self)
        layout.addWidget(self.execute_button)
    
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
        
        # 创建并添加对齐控制面板
        self.alignment_panel = AlignmentControlPanel(self)
        self.addWidget(self.alignment_panel)
    
    def connect_font_signals(self, font_changed_handler, size_changed_handler, color_clicked_handler, italic_clicked_handler=None):
        """
        连接字体控制相关信号
        """
        if self.font_panel:
            self.font_panel.connect_signals(
                font_changed_handler, 
                size_changed_handler, 
                color_clicked_handler,
                italic_clicked_handler
            )
    
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