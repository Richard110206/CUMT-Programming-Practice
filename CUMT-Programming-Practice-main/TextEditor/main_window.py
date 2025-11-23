#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口模块
负责创建应用程序的主窗口，整合文本编辑、文件操作和DeepSeek功能
"""

from PyQt5.QtWidgets import (
    QMainWindow,
    QAction,
    QFileDialog,
    QMessageBox,
    QDockWidget,
    QStatusBar,
    QApplication,
    QColorDialog,
    QSplitter,
    QLabel,
    QWidget,
    QVBoxLayout,
)
from PyQt5.QtGui import QIcon, QColor, QTextBlockFormat, QFont
from PyQt5.QtCore import Qt
import sys
import os

from text_editor import TextEditor
from file_operations import FileOperations
from deepseek_client import DeepSeekClient
from ui_components import MainToolBar, DeepSeekControlPanel, AIResultPanel


class MainWindow(QMainWindow):
    """
    主窗口类
    负责整个应用程序的UI布局和功能整合
    """
    def __init__(self):
        super().__init__()
        self.current_file_path = None
        self.current_theme = "light"  # 默认主题为浅色
        self.init_ui()

    def init_ui(self):
        """
        初始化用户界面
        """
        # 设置窗口基本属性
        self.setWindowTitle("文本编辑器")
        self.setGeometry(100, 100, 1200, 800)

        # 确保菜单栏在macOS上可见
        self.menuBar().setNativeMenuBar(False)

        # 创建核心组件
        self.text_editor = TextEditor(self)
        self.file_operations = FileOperations(self)
        self.deepseek_client = DeepSeekClient()

        # 创建多面板中心区域
        self.setup_central_panes()

        # 确保文本编辑器有正确的颜色设置
        self.ensure_text_editor_visibility()

        # 创建并添加工具栏
        self.toolbar = MainToolBar(self)
        self.addToolBar(self.toolbar)

        # 创建DeepSeek控制面板
        self.create_deepseek_dock()

        # 创建菜单栏
        self.create_menu_bar()

        # 创建状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.cursor_position_label = QLabel("行 1 列 1")
        self.statusBar.addPermanentWidget(self.cursor_position_label)
        self.statusBar.showMessage("就绪")

        # 连接信号和槽
        self.connect_signals_and_slots()

    def setup_central_panes(self):
        """
        创建文本编辑区域作为中心
        """
        # 文本编辑器作为中心部件
        self.setCentralWidget(self.text_editor)

    def ensure_text_editor_visibility(self):
        """
        确保文本编辑器有正确的颜色设置
        """
        # 强制设置文本编辑器的样式以确保可见性
        self.text_editor.setStyleSheet("""
            QTextEdit {
                background-color: white !important;
                color: #000000 !important;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                padding: 20px;
                font-size: 16px;
                line-height: 1.8;
                selection-background-color: #bbdefb;
                selection-color: #1565C0;
            }
            QTextEdit:focus {
                border-color: #2196F3;
            }
            QScrollBar:vertical {
                background: #f5f5f5;
                width: 12px;
                border-radius: 6px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #bdbdbd;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9e9e9e;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)

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

        # 视图菜单
        view_menu = menu_bar.addMenu("视图")

        # 主题切换子菜单
        theme_menu = view_menu.addMenu("主题")

        # 浅色主题
        light_theme_action = QAction("浅色", self)
        light_theme_action.triggered.connect(lambda: self.set_theme("light"))
        theme_menu.addAction(light_theme_action)

        # 深色主题
        dark_theme_action = QAction("深色", self)
        dark_theme_action.triggered.connect(lambda: self.set_theme("dark"))
        theme_menu.addAction(dark_theme_action)

    def create_deepseek_dock(self):
        """
        创建DeepSeek功能的停靠窗口，包含控制面板和AI结果展示
        """
        # 创建整合的面板容器
        combined_panel = QWidget(self)
        combined_layout = QVBoxLayout(combined_panel)
        combined_layout.setContentsMargins(6, 6, 6, 6)
        combined_layout.setSpacing(6)

        # DeepSeek控制面板
        self.deepseek_panel = DeepSeekControlPanel()
        combined_layout.addWidget(self.deepseek_panel)

        # 分隔线
        separator = QLabel(combined_panel)
        separator.setStyleSheet("""
            QLabel {
                background: #e0e0e0;
                height: 1px;
                border: none;
            }
        """)
        separator.setFixedHeight(1)
        combined_layout.addWidget(separator)

        # AI结果展示面板
        self.ai_result_panel = AIResultPanel(self)
        self.ai_result_panel.connect_control_signals(
            self.copy_ai_result_to_clipboard,
            self.clear_ai_result_panel,
        )
        self.ai_result_panel.apply_theme(self.current_theme)
        self.ai_result_display = self.ai_result_panel.text_edit
        ai_font = self.ai_result_display.font()
        ai_font.setPointSize(14)  # 设置更大的字体大小，提高可读性
        self.ai_result_display.setFont(ai_font)
        combined_layout.addWidget(self.ai_result_panel)

        # 创建停靠窗口
        self.deepseek_dock = QDockWidget("AI 助手", self)
        self.deepseek_dock.setWidget(combined_panel)

        # 添加停靠窗口到主窗口右侧
        self.addDockWidget(Qt.RightDockWidgetArea, self.deepseek_dock)

        # 设置停靠窗口可以移动和浮动，但默认紧凑
        self.deepseek_dock.setFeatures(QDockWidget.DockWidgetMovable |
                                     QDockWidget.DockWidgetFloatable)

        # 设置停靠窗口的初始大小 - 适应新的选项卡布局
        self.deepseek_dock.setMinimumWidth(280)
        self.deepseek_dock.setMaximumWidth(400)

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
        self.text_editor.cursorPositionChanged.connect(self.on_cursor_position_changed)

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
            self.ai_result_panel.set_text(result)
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
        else:
            if self.current_file_path:
                self.setWindowTitle(f"文本编辑器 - {self.current_file_path}")
            else:
                self.setWindowTitle("文本编辑器")

    def on_cursor_position_changed(self):
        """
        当光标位置改变时的处理函数
        """
        # 更新粗体和斜体按钮的状态
        is_bold = self.text_editor.has_bold_format()
        is_italic = self.text_editor.has_italic_format()

        # 阻止信号以避免递归
        self.toolbar.font_panel.bold_button.blockSignals(True)
        self.toolbar.font_panel.italic_button.blockSignals(True)

        # 更新粗体按钮状态
        if self.toolbar.font_panel.bold_button.isChecked() != is_bold:
            self.toolbar.font_panel.bold_button.setChecked(is_bold)

        # 更新斜体按钮状态
        if self.toolbar.font_panel.italic_button.isChecked() != is_italic:
            self.toolbar.font_panel.italic_button.setChecked(is_italic)

        # 恢复信号
        self.toolbar.font_panel.bold_button.blockSignals(False)
        self.toolbar.font_panel.italic_button.blockSignals(False)

        # 更新状态栏的光标位置
        self.update_cursor_position_label()

    def update_cursor_position_label(self):
        cursor = self.text_editor.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.positionInBlock() + 1
        self.cursor_position_label.setText(f"行 {line} 列 {column}")

    def copy_ai_result_to_clipboard(self):
        text = self.ai_result_panel.get_text().strip()
        if not text:
            self.statusBar.showMessage("无可复制的AI结果", 2000)
            return
        QApplication.clipboard().setText(text)
        self.statusBar.showMessage("AI结果已复制到剪贴板", 2000)

    def clear_ai_result_panel(self):
        self.ai_result_panel.clear_text()
        self.statusBar.showMessage("AI结果已清空", 2000)

    def set_theme(self, theme):
        """
        设置应用程序主题
        :param theme: 主题名称 ("light" 或 "dark")
        """
        self.current_theme = theme

        if theme == "light":
            # 清爽浅色主题
            self.setStyleSheet("""
                QMainWindow {
                    background: #f8f9fa;
                }
                QWidget {
                    background-color: transparent;
                    color: #212529;
                }
                QTextEdit {
                    background-color: white;
                    color: #212529;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                }
                QMenuBar {
                    background: white;
                    color: #212529;
                    border-bottom: 1px solid #dee2e6;
                    padding: 4px 8px;
                    font-size: 13px;
                }
                QMenuBar::item {
                    background: transparent;
                    padding: 6px 12px;
                    border-radius: 4px;
                    margin: 1px;
                }
                QMenuBar::item:selected {
                    background: #e3f2fd;
                    color: #1976D2;
                }
                QMenu {
                    background-color: white;
                    color: #212529;
                    border: 1px solid #dee2e6;
                    border-radius: 6px;
                    padding: 4px;
                }
                QMenu::item {
                    padding: 6px 12px;
                    border-radius: 4px;
                }
                QMenu::item:selected {
                    background-color: #e3f2fd;
                    color: #1976D2;
                }
                QDockWidget {
                    background-color: white;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                    font-size: 12px;
                }
                QDockWidget::title {
                    background: #f8f9fa;
                    color: #495057;
                    padding: 8px 12px;
                    border-bottom: 1px solid #dee2e6;
                    font-weight: 600;
                    font-size: 12px;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                }
                QDockWidget::close-button, QDockWidget::float-button {
                    background: transparent;
                    border: none;
                }
                QDockWidget::close-button:hover, QDockWidget::float-button:hover {
                    background: #e9ecef;
                    border-radius: 3px;
                }
                QStatusBar {
                    background: #f8f9fa;
                    color: #6c757d;
                    border-top: 1px solid #dee2e6;
                    font-size: 11px;
                }
                QStatusBar::item {
                    border: none;
                }
                QToolBar {
                    background: white;
                    border-bottom: 1px solid #dee2e6;
                    spacing: 6px;
                    padding: 6px 8px;
                }
                QToolBar::separator {
                    background: #dee2e6;
                    width: 1px;
                    margin: 4px 2px;
                }
            """)
            # 更新面板背景
            self.deepseek_panel.setStyleSheet("""
                DeepSeekControlPanel {
                    background: #fafafa;
                    border-radius: 6px;
                }
            """)
            self.ai_result_panel.apply_theme("light")
            # 重新应用文本编辑器的样式
            self.ensure_text_editor_visibility()
        else:
            # 现代深色主题
            self.setStyleSheet("""
                QMainWindow {
                    background: #1a1a1a;
                }
                QWidget {
                    background-color: transparent;
                    color: #e9ecef;
                }
                QTextEdit {
                    background-color: #2d3748;
                    color: #e9ecef;
                    border: 1px solid #4a5568;
                    border-radius: 8px;
                }
                QMenuBar {
                    background: #2d3748;
                    color: #e9ecef;
                    border-bottom: 1px solid #4a5568;
                    padding: 4px 8px;
                    font-size: 13px;
                }
                QMenuBar::item {
                    background: transparent;
                    padding: 6px 12px;
                    border-radius: 4px;
                    margin: 1px;
                }
                QMenuBar::item:selected {
                    background: #4a5568;
                    color: #90cdf4;
                }
                QMenu {
                    background-color: #2d3748;
                    color: #e9ecef;
                    border: 1px solid #4a5568;
                    border-radius: 6px;
                    padding: 4px;
                }
                QMenu::item {
                    padding: 6px 12px;
                    border-radius: 4px;
                }
                QMenu::item:selected {
                    background-color: #4a5568;
                    color: #90cdf4;
                }
                QDockWidget {
                    background-color: #2d3748;
                    border: 1px solid #4a5568;
                    border-radius: 8px;
                    font-size: 12px;
                }
                QDockWidget::title {
                    background: #1a202c;
                    color: #90cdf4;
                    padding: 8px 12px;
                    border-bottom: 1px solid #4a5568;
                    font-weight: 600;
                    font-size: 12px;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                }
                QDockWidget::close-button, QDockWidget::float-button {
                    background: transparent;
                    border: none;
                }
                QDockWidget::close-button:hover, QDockWidget::float-button:hover {
                    background: #4a5568;
                    border-radius: 3px;
                }
                QStatusBar {
                    background: #1a202c;
                    color: #a0aec0;
                    border-top: 1px solid #4a5568;
                    font-size: 11px;
                }
                QStatusBar::item {
                    border: none;
                }
                QToolBar {
                    background: #2d3748;
                    border-bottom: 1px solid #4a5568;
                    spacing: 6px;
                    padding: 6px 8px;
                }
                QToolBar::separator {
                    background: #4a5568;
                    width: 1px;
                    margin: 4px 2px;
                }
            """)
            # 更新面板背景
            self.deepseek_panel.setStyleSheet("""
                DeepSeekControlPanel {
                    background: #1a202c;
                    border-radius: 6px;
                }
            """)
            self.ai_result_panel.apply_theme("dark")
            # 重新应用深色主题的文本编辑器样式
            self.text_editor.setStyleSheet("""
                QTextEdit {
                    background-color: #2d3748 !important;
                    color: #e9ecef !important;
                    border: 1px solid #4a5568;
                    border-radius: 8px;
                    padding: 16px;
                    font-size: 14px;
                    line-height: 1.6;
                    selection-background-color: #4a5568;
                    selection-color: #90cdf4;
                }
                QTextEdit:focus {
                    border-color: #63b3ed;
                }
                QScrollBar:vertical {
                    background: #4a5568;
                    width: 10px;
                    border-radius: 5px;
                    margin: 0;
                }
                QScrollBar::handle:vertical {
                    background: #718096;
                    border-radius: 5px;
                    min-height: 15px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #a0aec0;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    border: none;
                    background: none;
                }
            """)

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