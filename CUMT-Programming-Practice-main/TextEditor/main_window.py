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
    QMdiArea,
    QMdiSubWindow,
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
        self.mdi_area = None
        self.sub_windows = []  # 存储所有子窗口
        self.window_counter = 0  # 用于为新窗口编号
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
        self.text_editor = None  # 现在使用MDI子窗口
        self.file_operations = FileOperations(self)
        self.deepseek_client = DeepSeekClient()

        # 创建多面板中心区域
        self.setup_central_panes()

        # MDI区域设置已在setup_central_panes中完成

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
        创建MDI区域和文本编辑窗口
        """
        # 创建MDI区域
        self.mdi_area = QMdiArea()
        self.mdi_area.setContentsMargins(0, 2, 0, 0)  # 减少顶部边距
        self.setCentralWidget(self.mdi_area)

        # 设置MDI区域的背景颜色和子窗口样式
        self.mdi_area.setStyleSheet("""
            QMdiArea {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
            QMdiSubWindow {
                background: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                margin: 1px;
            }
            QMdiSubWindow:focus {
                border-color: #2196F3;
                box-shadow: 0 0 0 1px rgba(33, 150, 243, 0.2);
            }
            QMdiSubWindow:titlebar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e2e8f0, stop:1 #cbd5e0);
                color: #000000;
                padding: 4px 8px;
                border-bottom: 1px solid #a0aec0;
                font-weight: 600;
                font-size: 13px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QMdiSubWindow::close-button, QMdiSubWindow::maximize-button, QMdiSubWindow::minimize-button {
                background: transparent;
                border: none;
                border-radius: 3px;
                padding: 2px;
                margin: 2px;
                color: #000000;
            }
            QMdiSubWindow::close-button:hover, QMdiSubWindow::maximize-button:hover, QMdiSubWindow::minimize-button:hover {
                background: #e9ecef;
                color: #000000;
            }
            QMdiSubWindow::close-button:pressed, QMdiSubWindow::maximize-button:pressed, QMdiSubWindow::minimize-button:pressed {
                background: #ced4da;
            }
        """)

        # 创建第一个文本编辑器窗口
        self.create_new_text_window("未命名-1")

    # 文本编辑器样式现在通过apply_theme方法管理

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

        # 窗口菜单
        window_menu = menu_bar.addMenu("窗口")

        # 新建窗口
        new_window_action = QAction("新建窗口", self)
        new_window_action.setShortcut("Ctrl+N")
        new_window_action.triggered.connect(self.new_window)
        window_menu.addAction(new_window_action)

        # 添加分隔线
        window_menu.addSeparator()

        # 层叠窗口
        cascade_action = QAction("层叠窗口", self)
        cascade_action.triggered.connect(self.cascade_windows)
        window_menu.addAction(cascade_action)

        # 平铺窗口
        tile_action = QAction("平铺窗口", self)
        tile_action.triggered.connect(self.tile_windows)
        window_menu.addAction(tile_action)

        # 水平平铺
        tile_horizontal_action = QAction("水平平铺", self)
        tile_horizontal_action.triggered.connect(self.tile_horizontal)
        window_menu.addAction(tile_horizontal_action)

        # 垂直平铺
        tile_vertical_action = QAction("垂直平铺", self)
        tile_vertical_action.triggered.connect(self.tile_vertical)
        window_menu.addAction(tile_vertical_action)

        # 添加分隔线
        window_menu.addSeparator()

        # 关闭所有窗口
        close_all_action = QAction("关闭所有窗口", self)
        close_all_action.triggered.connect(self.close_all_windows)
        window_menu.addAction(close_all_action)

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
        ai_font.setPointSize(17)  # 设置更大的字体大小，提高可读性（增大3号）
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

        # 文本编辑器信号连接现在在create_new_text_window方法中处理

    def new_file(self):
        """
        新建文件
        """
        active_editor = self.get_active_editor()
        if active_editor:
            # 使用文件操作类新建文件
            self.file_operations.new_file(active_editor)
            # 获取当前活动窗口并更新标题
            active_window = self.mdi_area.activeSubWindow()
            if active_window:
                active_window.setWindowTitle("未命名")
            self.statusBar.showMessage("新建文件")

    def open_file(self):
        """
        打开文件
        """
        active_editor = self.get_active_editor()
        if not active_editor:
            return

        # 检查是否需要保存当前文件
        if active_editor.document().isModified():
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
        result = self.file_operations.open_file(active_editor)
        if result and self.file_operations.get_current_file_path():
            file_path = self.file_operations.get_current_file_path()
            # 更新当前活动窗口的标题
            active_window = self.mdi_area.activeSubWindow()
            if active_window:
                active_window.setWindowTitle(os.path.basename(file_path))
            self.statusBar.showMessage(f"已打开文件: {file_path}")

    def save_file(self):
        """
        保存文件
        :return: 是否保存成功
        """
        active_editor = self.get_active_editor()
        if not active_editor:
            return False

        # 获取当前活动窗口
        active_window = self.mdi_area.activeSubWindow()

        # 查找对应的文件路径
        file_path = None
        if active_window:
            for window_info in self.sub_windows:
                if window_info['window'] == active_window:
                    file_path = window_info['file_path']
                    break

        if file_path is None:
            return self.save_file_as()

        # 使用文件操作类保存文件
        result = self.file_operations.save_file(active_editor, file_path)
        if result:
            # 更新窗口信息中的文件路径
            if active_window:
                for window_info in self.sub_windows:
                    if window_info['window'] == active_window:
                        window_info['file_path'] = file_path
                        break
                active_window.setWindowTitle(os.path.basename(file_path))
            self.statusBar.showMessage(f"已保存文件: {file_path}")
            return True
        else:
            QMessageBox.critical(self, "错误", "保存文件失败")
            return False

    def save_file_as(self):
        """
        另存为文件
        :return: 是否保存成功
        """
        active_editor = self.get_active_editor()
        if not active_editor:
            return False

        # 使用文件操作类另存为文件
        result = self.file_operations.save_file_as(active_editor)
        if result and self.file_operations.get_current_file_path():
            file_path = self.file_operations.get_current_file_path()
            # 更新窗口信息中的文件路径
            active_window = self.mdi_area.activeSubWindow()
            if active_window:
                for window_info in self.sub_windows:
                    if window_info['window'] == active_window:
                        window_info['file_path'] = file_path
                        break
                active_window.setWindowTitle(os.path.basename(file_path))
            self.statusBar.showMessage(f"已保存文件: {file_path}")
        return result

    def change_font(self, font_name):
        """
        改变字体
        :param font_name: 字体名称
        """
        active_editor = self.get_active_editor()
        if active_editor:
            active_editor.set_text_font(font_name)

    def change_font_size(self, size_str):
        """
        改变字体大小
        :param size_str: 字号字符串
        """
        active_editor = self.get_active_editor()
        if active_editor:
            active_editor.set_text_size(size_str)

    def change_text_color(self):
        """
        改变文本颜色
        """
        active_editor = self.get_active_editor()
        if active_editor:
            color = QColorDialog.getColor()
            if color.isValid():
                active_editor.set_text_color(color)

    def change_first_line_indent(self, indent_type):
        """
        改变首行缩进
        :param indent_type: 缩进类型
        """
        active_editor = self.get_active_editor()
        if active_editor:
            active_editor.set_first_line_indent(indent_type)

    def change_line_spacing(self, spacing_type):
        """
        改变行间距
        :param spacing_type: 行间距类型
        """
        active_editor = self.get_active_editor()
        if active_editor:
            active_editor.set_line_spacing(spacing_type)


    def align_left(self):
        """
        左对齐
        """
        active_editor = self.get_active_editor()
        if active_editor:
            active_editor.set_alignment(Qt.AlignLeft)

    def align_center(self):
        """
        居中对齐
        """
        active_editor = self.get_active_editor()
        if active_editor:
            active_editor.set_alignment(Qt.AlignCenter)

    def align_right(self):
        """
        右对齐
        """
        active_editor = self.get_active_editor()
        if active_editor:
            active_editor.set_alignment(Qt.AlignRight)

    def undo(self):
        """
        撤销操作
        """
        active_editor = self.get_active_editor()
        if active_editor:
            active_editor.undo()

    def redo(self):
        """
        重做操作
        """
        active_editor = self.get_active_editor()
        if active_editor:
            active_editor.redo()

    def cut(self):
        """
        剪切操作
        """
        active_editor = self.get_active_editor()
        if active_editor:
            active_editor.cut()

    def copy(self):
        """
        复制操作
        """
        active_editor = self.get_active_editor()
        if active_editor:
            active_editor.copy()

    def paste(self):
        """
        粘贴操作
        """
        active_editor = self.get_active_editor()
        if active_editor:
            active_editor.paste()

    def execute_deepseek_function(self):
        """
        执行DeepSeek功能
        """
        active_editor = self.get_active_editor()
        if not active_editor:
            return

        function_name = self.deepseek_panel.get_selected_function()
        current_text = active_editor.toPlainText()

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
        active_editor = self.get_active_editor()
        if active_editor:
            active_editor.set_bold()

    def toggle_italic(self):
        """
        切换斜体状态
        """
        active_editor = self.get_active_editor()
        if active_editor:
            active_editor.set_italic()

    def on_text_changed(self):
        """
        当文本内容改变时的处理函数
        """
        active_editor = self.get_active_editor()
        if not active_editor:
            return

        # 更新当前活动窗口标题，添加*表示有未保存的修改
        active_window = self.mdi_area.activeSubWindow()
        if active_window and active_editor.document().isModified():
            current_title = active_window.windowTitle()
            if not current_title.endswith(" *"):
                active_window.setWindowTitle(current_title + " *")
        elif active_window and not active_editor.document().isModified():
            current_title = active_window.windowTitle()
            if current_title.endswith(" *"):
                active_window.setWindowTitle(current_title[:-2])

    def on_cursor_position_changed(self):
        """
        当光标位置改变时的处理函数
        """
        active_editor = self.get_active_editor()
        if not active_editor:
            return

        # 更新粗体和斜体按钮的状态
        is_bold = active_editor.has_bold_format()
        is_italic = active_editor.has_italic_format()

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
        active_editor = self.get_active_editor()
        if not active_editor:
            return

        cursor = active_editor.textCursor()
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
                    color: #2d3748;
                }
                QTextEdit {
                    background-color: white;
                    color: #2d3748;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                }
                QMenuBar {
                    background: white;
                    color: #2d3748;
                    border-bottom: 1px solid #dee2e6;
                    padding: 6px 12px;
                    font-size: 17px;
                    font-weight: 500;
                }
                QMenuBar::item {
                    background: transparent;
                    padding: 8px 16px;
                    border-radius: 4px;
                    margin: 1px;
                    font-size: 17px;
                    font-weight: 500;
                }
                QMenuBar::item:selected {
                    background: #ebf8ff;
                    color: #2b6cb0;
                }
                QMenu {
                    background-color: white;
                    color: #2d3748;
                    border: 1px solid #dee2e6;
                    border-radius: 6px;
                    padding: 4px;
                }
                QMenu::item {
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-size: 16px;
                    font-weight: 500;
                }
                QMenu::item:selected {
                    background-color: #ebf8ff;
                    color: #2b6cb0;
                }
                QDockWidget {
                    background-color: white;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                    font-size: 12px;
                }
                QDockWidget:hover {
                    border-color: #3182ce;
                    box-shadow: 0 0 0 1px rgba(49, 130, 206, 0.1);
                }
                QDockWidget::title {
                    background: #f8f9fa;
                    color: #4a5568;
                    padding: 8px 12px;
                    border-bottom: 1px solid #dee2e6;
                    font-weight: 600;
                    font-size: 13px;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                }
                QDockWidget::close-button, QDockWidget::float-button {
                    background: transparent;
                    border: none;
                }
                QDockWidget::close-button:hover, QDockWidget::float-button:hover {
                    background: #e2e8f0;
                    border-radius: 3px;
                }
                QStatusBar {
                    background: #f8f9fa;
                    color: #718096;
                    border-top: 1px solid #dee2e6;
                    font-size: 12px;
                    font-weight: 500;
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
            # 对所有窗口应用主题
            for window_info in self.sub_windows:
                editor = window_info['editor']
                if editor:
                    editor.apply_theme("light")

            # 更新MDI子窗口标题样式
            self.mdi_area.setStyleSheet("""
                QMdiArea {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #f8f9fa, stop:1 #e9ecef);
                }
                QMdiSubWindow {
                    background: white;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                    margin: 1px;
                }
                QMdiSubWindow:focus {
                    border-color: #2196F3;
                    box-shadow: 0 0 0 1px rgba(33, 150, 243, 0.2);
                }
                QMdiSubWindow:titlebar {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #e2e8f0, stop:1 #cbd5e0);
                    color: #000000;
                    padding: 4px 8px;
                    border-bottom: 1px solid #a0aec0;
                    font-weight: 600;
                    font-size: 13px;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                }
                QMdiSubWindow::close-button, QMdiSubWindow::maximize-button, QMdiSubWindow::minimize-button {
                    background: transparent;
                    border: none;
                    border-radius: 3px;
                    padding: 2px;
                    margin: 2px;
                }
                QMdiSubWindow::close-button:hover, QMdiSubWindow::maximize-button:hover, QMdiSubWindow::minimize-button:hover {
                    background: #e9ecef;
                }
                QMdiSubWindow::close-button:pressed, QMdiSubWindow::maximize-button:pressed, QMdiSubWindow::minimize-button:pressed {
                    background: #ced4da;
                }
            """)
        else:
            # 现代深色主题
            self.setStyleSheet("""
                QMainWindow {
                    background: #1a202c;
                }
                QWidget {
                    background-color: transparent;
                    color: #e2e8f0;
                }
                QTextEdit {
                    background-color: #2d3748;
                    color: #e2e8f0;
                    border: 1px solid #4a5568;
                    border-radius: 8px;
                }
                QMenuBar {
                    background: #2d3748;
                    color: #e2e8f0;
                    border-bottom: 1px solid #4a5568;
                    padding: 6px 12px;
                    font-size: 17px;
                    font-weight: 500;
                }
                QMenuBar::item {
                    background: transparent;
                    padding: 8px 16px;
                    border-radius: 4px;
                    margin: 1px;
                    font-size: 17px;
                    font-weight: 500;
                }
                QMenuBar::item:selected {
                    background: #4a5568;
                    color: #90cdf4;
                }
                QMenu {
                    background-color: #2d3748;
                    color: #e2e8f0;
                    border: 1px solid #4a5568;
                    border-radius: 6px;
                    padding: 4px;
                }
                QMenu::item {
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-size: 16px;
                    font-weight: 500;
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
                QDockWidget:hover {
                    border-color: #4299e1;
                    box-shadow: 0 0 0 1px rgba(66, 153, 225, 0.2);
                }
                QDockWidget::title {
                    background: #1a202c;
                    color: #90cdf4;
                    padding: 8px 12px;
                    border-bottom: 1px solid #4a5568;
                    font-weight: 600;
                    font-size: 13px;
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
                    font-size: 13px;
                    font-weight: 500;
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
            # 对所有窗口应用深色主题
            for window_info in self.sub_windows:
                editor = window_info['editor']
                if editor:
                    editor.apply_theme("dark")

            # 更新MDI子窗口标题样式（深色主题）
            self.mdi_area.setStyleSheet("""
                QMdiArea {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #1a202c, stop:1 #2d3748);
                }
                QMdiSubWindow {
                    background: #2d3748;
                    border: 1px solid #4a5568;
                    border-radius: 8px;
                    margin: 1px;
                }
                QMdiSubWindow:focus {
                    border-color: #4299e1;
                    box-shadow: 0 0 0 1px rgba(66, 153, 225, 0.2);
                }
                QMdiSubWindow:titlebar {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #4a5568, stop:1 #2d3748);
                    color: #f7fafc;
                    padding: 4px 8px;
                    border-bottom: 1px solid #718096;
                    font-weight: 600;
                    font-size: 13px;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                }
                QMdiSubWindow::close-button, QMdiSubWindow::maximize-button, QMdiSubWindow::minimize-button {
                    background: transparent;
                    border: none;
                    border-radius: 3px;
                    padding: 2px;
                    margin: 2px;
                    color: #f7fafc;
                }
                QMdiSubWindow::close-button:hover, QMdiSubWindow::maximize-button:hover, QMdiSubWindow::minimize-button:hover {
                    background: #718096;
                    color: #f7fafc;
                }
                QMdiSubWindow::close-button:pressed, QMdiSubWindow::maximize-button:pressed, QMdiSubWindow::minimize-button:pressed {
                    background: #4a5568;
                }
            """)

    def closeEvent(self, event):
        """
        关闭窗口时的事件处理
        :param event: 事件对象
        """
        # 检查所有窗口是否有未保存的更改
        unsaved_windows = []
        for window_info in self.sub_windows:
            editor = window_info['editor']
            if editor and editor.document().isModified():
                unsaved_windows.append(window_info)

        if unsaved_windows:
            response = QMessageBox.question(
                self,
                "保存",
                f"有 {len(unsaved_windows)} 个窗口包含未保存的更改，是否保存？",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )

            if response == QMessageBox.Cancel:
                event.ignore()
                return
            elif response == QMessageBox.Yes:
                # 保存所有未保存的窗口
                for window_info in unsaved_windows:
                    # 设置为活动窗口并保存
                    self.mdi_area.setActiveSubWindow(window_info['window'])
                    if not self.save_file():
                        event.ignore()
                        return

        event.accept()

    def create_new_text_window(self, title=None):
        """
        创建新的文本编辑器窗口
        :param title: 窗口标题，如果为None则自动生成
        """
        if title is None:
            self.window_counter += 1
            title = f"未命名-{self.window_counter}"

        # 创建新的文本编辑器实例
        new_text_editor = TextEditor(self)
        new_text_editor.apply_theme(self.current_theme)

        # 创建MDI子窗口
        sub_window = QMdiSubWindow()
        sub_window.setWidget(new_text_editor)
        sub_window.setWindowTitle(title)
        sub_window.resize(600, 400)

        # 将子窗口添加到MDI区域
        self.mdi_area.addSubWindow(sub_window)

        # 立即应用当前主题的MDI窗口样式
        self.apply_mdi_window_theme()

        # 存储窗口信息
        self.sub_windows.append({
            'window': sub_window,
            'editor': new_text_editor,
            'title': title,
            'file_path': None
        })

        # 连接信号
        new_text_editor.textChanged.connect(self.on_text_changed)
        new_text_editor.cursorPositionChanged.connect(self.on_cursor_position_changed)

        # 显示窗口
        sub_window.show()

        # 设置为活动窗口
        self.mdi_area.setActiveSubWindow(sub_window)

        return sub_window

    def apply_mdi_window_theme(self):
        """
        应用MDI窗口的主题样式
        """
        if self.current_theme == "light":
            # 浅色主题MDI窗口样式
            mdi_style = """
                QMdiArea {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #f8f9fa, stop:1 #e9ecef);
                }
                QMdiSubWindow {
                    background: white;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                    margin: 1px;
                }
                QMdiSubWindow:focus {
                    border-color: #2196F3;
                    box-shadow: 0 0 0 1px rgba(33, 150, 243, 0.2);
                }
                QMdiSubWindow:titlebar {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #e2e8f0, stop:1 #cbd5e0);
                    color: #000000;
                    padding: 4px 8px;
                    border-bottom: 1px solid #a0aec0;
                    font-weight: 600;
                    font-size: 13px;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                }
                QMdiSubWindow::close-button, QMdiSubWindow::maximize-button, QMdiSubWindow::minimize-button {
                    background: transparent;
                    border: none;
                    border-radius: 3px;
                    padding: 2px;
                    margin: 2px;
                    color: #1a202c;
                }
                QMdiSubWindow::close-button:hover, QMdiSubWindow::maximize-button:hover, QMdiSubWindow::minimize-button:hover {
                    background: #e9ecef;
                    color: #1a202c;
                }
                QMdiSubWindow::close-button:pressed, QMdiSubWindow::maximize-button:pressed, QMdiSubWindow::minimize-button:pressed {
                    background: #ced4da;
                }
            """
        else:
            # 深色主题MDI窗口样式
            mdi_style = """
                QMdiArea {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #1a202c, stop:1 #2d3748);
                }
                QMdiSubWindow {
                    background: #2d3748;
                    border: 1px solid #4a5568;
                    border-radius: 8px;
                    margin: 1px;
                }
                QMdiSubWindow:focus {
                    border-color: #4299e1;
                    box-shadow: 0 0 0 1px rgba(66, 153, 225, 0.2);
                }
                QMdiSubWindow:titlebar {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #4a5568, stop:1 #2d3748);
                    color: #f7fafc;
                    padding: 4px 8px;
                    border-bottom: 1px solid #718096;
                    font-weight: 600;
                    font-size: 13px;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                }
                QMdiSubWindow::close-button, QMdiSubWindow::maximize-button, QMdiSubWindow::minimize-button {
                    background: transparent;
                    border: none;
                    border-radius: 3px;
                    padding: 2px;
                    margin: 2px;
                    color: #f7fafc;
                }
                QMdiSubWindow::close-button:hover, QMdiSubWindow::maximize-button:hover, QMdiSubWindow::minimize-button:hover {
                    background: #718096;
                    color: #f7fafc;
                }
                QMdiSubWindow::close-button:pressed, QMdiSubWindow::maximize-button:pressed, QMdiSubWindow::minimize-button:pressed {
                    background: #4a5568;
                }
            """

        self.mdi_area.setStyleSheet(mdi_style)

    def new_window(self):
        """
        新建窗口
        """
        self.window_counter += 1
        self.create_new_text_window(f"未命名-{self.window_counter}")
        self.statusBar.showMessage(f"新建窗口: 未命名-{self.window_counter}")

    def cascade_windows(self):
        """
        层叠窗口
        """
        self.mdi_area.cascadeSubWindows()
        self.statusBar.showMessage("窗口已层叠")

    def tile_windows(self):
        """
        平铺窗口
        """
        self.mdi_area.tileSubWindows()
        self.statusBar.showMessage("窗口已平铺")

    def tile_horizontal(self):
        """
        水平平铺窗口
        """
        if not self.sub_windows:
            return

        # 获取MDI区域的尺寸
        mdi_rect = self.mdi_area.rect()
        window_width = mdi_rect.width() // len(self.sub_windows)
        window_height = mdi_rect.height()

        for i, window_info in enumerate(self.sub_windows):
            window = window_info['window']
            if window and not window.isClosed():
                window.resize(window_width, window_height)
                window.move(i * window_width, 0)

        self.statusBar.showMessage("窗口已水平平铺")

    def tile_vertical(self):
        """
        垂直平铺窗口
        """
        if not self.sub_windows:
            return

        # 获取MDI区域的尺寸
        mdi_rect = self.mdi_area.rect()
        window_width = mdi_rect.width()
        window_height = mdi_rect.height() // len(self.sub_windows)

        for i, window_info in enumerate(self.sub_windows):
            window = window_info['window']
            if window and not window.isClosed():
                window.resize(window_width, window_height)
                window.move(0, i * window_height)

        self.statusBar.showMessage("窗口已垂直平铺")

    def close_all_windows(self):
        """
        关闭所有窗口（除了第一个）
        """
        if len(self.sub_windows) <= 1:
            return

        # 检查是否有未保存的文件
        unsaved_count = 0
        for window_info in self.sub_windows[1:]:
            editor = window_info['editor']
            if editor and editor.document().isModified():
                unsaved_count += 1

        if unsaved_count > 0:
            response = QMessageBox.question(
                self,
                "保存文件",
                f"有 {unsaved_count} 个窗口包含未保存的更改，是否保存？",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )

            if response == QMessageBox.Cancel:
                return
            elif response == QMessageBox.Yes:
                # 这里可以添加保存逻辑
                pass

        # 关闭除第一个窗口外的所有窗口
        for window_info in self.sub_windows[1:]:
            window = window_info['window']
            if window and not window.isClosed():
                window.close()

        # 清理已关闭的窗口信息
        self.sub_windows = [w for w in self.sub_windows if w['window'] and not w['window'].isClosed()]

        self.statusBar.showMessage("已关闭其他窗口")

    def get_active_editor(self):
        """
        获取当前活动的文本编辑器
        """
        active_window = self.mdi_area.activeSubWindow()
        if active_window:
            for window_info in self.sub_windows:
                if window_info['window'] == active_window:
                    return window_info['editor']

        # 如果没有活动窗口，返回第一个编辑器
        if self.sub_windows:
            return self.sub_windows[0]['editor']

        return None