#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口模块
负责创建应用程序的主窗口，整合文本编辑、文件操作和DeepSeek功能
"""

from PyQt5.QtWidgets import (QMainWindow, QAction, QFileDialog, QMessageBox, 
                           QDockWidget, QStatusBar, QApplication, QColorDialog, 
                           QTextEdit)
from PyQt5.QtGui import QIcon, QColor, QTextBlockFormat
from PyQt5.QtCore import Qt
import sys
import os

from text_editor import TextEditor
from file_operations import FileOperations
from deepseek_client import DeepSeekClient
from ui_components import MainToolBar, DeepSeekControlPanel


class MainWindow(QMainWindow):
    """
    主窗口类
    负责整个应用程序的UI布局和功能整合
    """
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_file_path = None
    
    def init_ui(self):
        """
        初始化用户界面
        """
        # 设置窗口基本属性
        self.setWindowTitle("文本编辑器")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建核心组件
        self.text_editor = TextEditor(self)
        self.file_operations = FileOperations(self)
        self.deepseek_client = DeepSeekClient()
        
        # 创建AI结果展示区域
        self.ai_result_display = QTextEdit(self)
        self.ai_result_display.setReadOnly(True)
        self.ai_result_display.setWindowTitle("AI结果展示")
        
        # 设置中心组件为文本编辑器
        self.setCentralWidget(self.text_editor)
        
        # 创建并添加工具栏
        self.toolbar = MainToolBar(self)
        self.addToolBar(self.toolbar)
        
        # 创建DeepSeek控制面板
        self.create_deepseek_dock()
        
        # 创建AI结果展示面板
        self.create_ai_result_dock()
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("就绪")
        
        # 连接信号和槽
        self.connect_signals_and_slots()
    
    def create_menu_bar(self):
        """
        创建菜单栏
        """
        menu_bar = self.menuBar()
        
        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        
        # 新建文件动作
        new_action = QAction("新建", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        # 打开文件动作
        open_action = QAction("打开", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        # 保存文件动作
        save_action = QAction("保存", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        # 另存为动作
        save_as_action = QAction("另存为...", self)
        save_as_action.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_action)
        
        # 添加分隔线
        file_menu.addSeparator()
        
        # 退出动作
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menu_bar.addMenu("编辑")
        
        # 撤销动作
        undo_action = QAction("撤销", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)
        
        # 重做动作
        redo_action = QAction("重做", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        # 添加分隔线
        edit_menu.addSeparator()
        
        # 剪切动作
        cut_action = QAction("剪切", self)
        cut_action.setShortcut("Ctrl+X")
        cut_action.triggered.connect(self.cut)
        edit_menu.addAction(cut_action)
        
        # 复制动作
        copy_action = QAction("复制", self)
        copy_action.setShortcut("Ctrl+C")
        copy_action.triggered.connect(self.copy)
        edit_menu.addAction(copy_action)
        
        # 粘贴动作
        paste_action = QAction("粘贴", self)
        paste_action.setShortcut("Ctrl+V")
        paste_action.triggered.connect(self.paste)
        edit_menu.addAction(paste_action)
        
        # 添加分隔线
        edit_menu.addSeparator()
        
        # 粗体动作
        bold_action = QAction("粗体", self)
        bold_action.setShortcut("Ctrl+B")
        bold_action.triggered.connect(self.toggle_bold)
        edit_menu.addAction(bold_action)
        
        # 斜体动作
        italic_action = QAction("斜体", self)
        italic_action.setShortcut("Ctrl+I")
        italic_action.triggered.connect(self.toggle_italic)
        edit_menu.addAction(italic_action)
    
    def create_deepseek_dock(self):
        """
        创建DeepSeek功能的停靠窗口
        """
        self.deepseek_dock = QDockWidget("DeepSeek功能", self)
        self.deepseek_panel = DeepSeekControlPanel()
        
        # 设置停靠窗口的小部件
        self.deepseek_dock.setWidget(self.deepseek_panel)
        
        # 添加停靠窗口到主窗口右侧
        self.addDockWidget(Qt.RightDockWidgetArea, self.deepseek_dock)
        
        # 设置停靠窗口可以移动和浮动
        self.deepseek_dock.setFeatures(QDockWidget.DockWidgetMovable | 
                                     QDockWidget.DockWidgetFloatable)
    
    def create_ai_result_dock(self):
        """
        创建AI结果展示的停靠窗口
        """
        self.ai_result_dock = QDockWidget("AI结果展示", self)
        self.ai_result_dock.setWidget(self.ai_result_display)
        
        # 添加停靠窗口到主窗口右侧
        self.addDockWidget(Qt.RightDockWidgetArea, self.ai_result_dock)
        
        # 设置停靠窗口可以移动和浮动
        self.ai_result_dock.setFeatures(QDockWidget.DockWidgetMovable | 
                                       QDockWidget.DockWidgetFloatable)
    
    def connect_signals_and_slots(self):
        """
        连接信号和槽函数
        """
        # 连接工具栏信号
        self.toolbar.connect_font_signals(
            self.change_font,
            self.change_font_size,
            self.change_text_color,
            self.toggle_bold,
            self.toggle_italic
        )
        
        # 连接格式控制信号
        self.toolbar.connect_format_signals(
            self.change_first_line_indent,
            self.change_line_spacing
        )
        

        # 连接对齐方式信号
        self.toolbar.connect_alignment_signals(
            self.align_left,
            self.align_center,
            self.align_right
        )
        
        # 连接DeepSeek面板信号
        self.deepseek_panel.connect_signals(self.execute_deepseek_function)
        
        # 连接文本编辑器内容改变信号
        self.text_editor.textChanged.connect(self.on_text_changed)
    
    def new_file(self):
        """
        新建文件
        """
        # 使用文件操作类新建文件
        self.file_operations.new_file(self.text_editor)
        self.current_file_path = None
        self.setWindowTitle("文本编辑器")
        self.statusBar.showMessage("新建文件")
    
    def open_file(self):
        """
        打开文件
        """
        # 检查是否需要保存当前文件
        if self.text_editor.document().isModified():
            response = QMessageBox.question(
                self, 
                "保存", 
                "是否保存当前文件？",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            
            if response == QMessageBox.Cancel:
                return
            elif response == QMessageBox.Yes:
                if not self.save_file():
                    return
        
        # 使用文件操作类打开文件
        result = self.file_operations.open_file(self.text_editor)
        if result and self.file_operations.get_current_file_path():
            self.current_file_path = self.file_operations.get_current_file_path()
            self.setWindowTitle(f"文本编辑器 - {os.path.basename(self.current_file_path)}")
            self.statusBar.showMessage(f"已打开文件: {self.current_file_path}")
    
    def save_file(self):
        """
        保存文件
        :return: 是否保存成功
        """
        if self.current_file_path is None:
            return self.save_file_as()
        
        # 使用文件操作类保存文件
        result = self.file_operations.save_file(self.text_editor)
        if result:
            self.current_file_path = self.file_operations.get_current_file_path()
            if self.current_file_path:
                self.setWindowTitle(f"文本编辑器 - {os.path.basename(self.current_file_path)}")
                self.statusBar.showMessage(f"已保存文件: {self.current_file_path}")
            return True
        else:
            QMessageBox.critical(self, "错误", "保存文件失败")
            return False
    
    def save_file_as(self):
        """
        另存为文件
        :return: 是否保存成功
        """
        # 使用文件操作类另存为文件
        result = self.file_operations.save_file_as(self.text_editor)
        if result and self.file_operations.get_current_file_path():
            self.current_file_path = self.file_operations.get_current_file_path()
            self.setWindowTitle(f"文本编辑器 - {os.path.basename(self.current_file_path)}")
            self.statusBar.showMessage(f"已保存文件: {self.current_file_path}")
        return result
    
    def change_font(self, font_name):
        """
        改变字体
        :param font_name: 字体名称
        """
        self.text_editor.set_text_font(font_name)
    
    def change_font_size(self, size_str):
        """
        改变字体大小
        :param size_str: 字号字符串
        """
        self.text_editor.set_text_size(size_str)
    
    def change_text_color(self):
        """
        改变文本颜色
        """
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_editor.set_text_color(color)
    
    def change_first_line_indent(self, indent_type):
        """
        改变首行缩进
        :param indent_type: 缩进类型
        """
        self.text_editor.set_first_line_indent(indent_type)
    
    def change_line_spacing(self, spacing_type):
        """
        改变行间距
        :param spacing_type: 行间距类型
        """
        self.text_editor.set_line_spacing(spacing_type)
    

    def align_left(self):
        """
        左对齐
        """
        self.text_editor.set_alignment(Qt.AlignLeft)
    
    def align_center(self):
        """
        居中对齐
        """
        self.text_editor.set_alignment(Qt.AlignCenter)
    
    def align_right(self):
        """
        右对齐
        """
        self.text_editor.set_alignment(Qt.AlignRight)
    
    def undo(self):
        """
        撤销操作
        """
        self.text_editor.undo()
    
    def redo(self):
        """
        重做操作
        """
        self.text_editor.redo()
    
    def cut(self):
        """
        剪切操作
        """
        self.text_editor.cut()
    
    def copy(self):
        """
        复制操作
        """
        self.text_editor.copy()
    
    def paste(self):
        """
        粘贴操作
        """
        self.text_editor.paste()
    
    def execute_deepseek_function(self):
        """
        执行DeepSeek功能
        """
        function_name = self.deepseek_panel.get_selected_function()
        current_text = self.text_editor.toPlainText()
        
        if not current_text.strip():
            QMessageBox.warning(self, "警告", "请先输入文本内容")
            return
        
        try:
            self.statusBar.showMessage(f"正在处理 {function_name}...")
            
            # 生成提示文本
            prompt = self.deepseek_client.generate_prompt(function_name, current_text)
            
            # 调用API
            result = self.deepseek_client.call_api(function_name, prompt)
            
            # 将结果显示在AI结果展示区域而不是直接插入正文中
            self.ai_result_display.setPlainText(result)
            self.statusBar.showMessage(f"{function_name}完成")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"DeepSeek API调用失败: {str(e)}")
            self.statusBar.showMessage("就绪")
            
    def toggle_bold(self):
        """
        切换粗体状态
        """
        self.text_editor.set_bold()
    
    def toggle_italic(self):
        """
        切换斜体状态
        """
        self.text_editor.set_italic()
    
    def on_text_changed(self):
        """
        当文本内容改变时的处理函数
        """
        # 更新窗口标题，添加*表示有未保存的修改
        if self.text_editor.document().isModified():
            if self.current_file_path:
                self.setWindowTitle(f"文本编辑器 - {self.current_file_path} *")
            else:
                self.setWindowTitle("文本编辑器 *")
    
    def closeEvent(self, event):
        """
        关闭窗口时的事件处理
        :param event: 事件对象
        """
        # 检查是否需要保存当前文件
        if self.text_editor.document().isModified():
            response = QMessageBox.question(
                self, 
                "保存", 
                "是否保存当前文件？",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            
            if response == QMessageBox.Cancel:
                event.ignore()
                return
            elif response == QMessageBox.Yes:
                if not self.save_file():
                    event.ignore()
                    return
        
        event.accept()