#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本编辑器核心功能模块
负责文本编辑、格式控制等基础功能
"""

from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QTextCursor, QTextBlockFormat


class TextEditor(QTextEdit):
    """
    文本编辑器类
    负责文本编辑功能的实现
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # 设置默认字体
        default_font = QFont()
        default_font.setPointSize(18)
        # 使用系统可用的字体，避免SimSun警告
        default_font.setFamily("PingFang SC" if "PingFang SC" in [family.family() for family in QFont().families()] else "Helvetica")
        self.setFont(default_font)

        # 设置Tab宽度为4个空格（兼容不同Qt版本）
        metrics = self.fontMetrics()
        space_width = (
            metrics.horizontalAdvance(' ')
            if hasattr(metrics, "horizontalAdvance")
            else metrics.width(' ')
        )
        tab_distance = space_width * 4
        if hasattr(self, "setTabStopDistance"):
            self.setTabStopDistance(tab_distance)
        else:
            self.setTabStopWidth(tab_distance)

        # 支持自动换行
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        # 支持撤销/重做功能
        self.setUndoRedoEnabled(True)

        # 提示文本
        self.setPlaceholderText("开始创作吧... 支持富文本编辑与AI辅助，享受流畅的写作体验！")

        # 初始化编辑模式
        self.edit_mode = "普通模式"

        # 设置现代化样式
        self.setStyleSheet("""
            QTextEdit {
                background: #ffffff;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 20px;
                font-size: 16px;
                line-height: 1.8;
                color: #2d3748;
                selection-background-color: #3182ce;
                selection-color: #ffffff;
            }
            QTextEdit:focus {
                border-color: #3182ce;
                box-shadow: 0 0 0 1px rgba(49, 130, 206, 0.1);
            }
            QScrollBar:vertical {
                background: #f7fafc;
                width: 12px;
                border-radius: 6px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: #cbd5e0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0aec0;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
    def set_text_font(self, font_family):
        """
        设置文本字体
        :param font_family: 字体名称
        """
        # 应用到选中文本
        cursor = self.textCursor()
        if not cursor.hasSelection():
            # 如果没有选中文本，设置后续输入文本的字体
            format_ = cursor.charFormat()
            format_.setFontFamily(font_family)
            cursor.setCharFormat(format_)
            return
        format_ = cursor.charFormat()
        format_.setFontFamily(font_family)
        cursor.setCharFormat(format_)
        
    def set_text_size(self, size):
        """
        设置文本字号
        :param size: 字号大小
        """
        try:
            size_int = int(size)
            # 应用到选中文本
            cursor = self.textCursor()
            if not cursor.hasSelection():
                # 如果没有选中文本，设置后续输入文本的字号
                format_ = cursor.charFormat()
                format_.setFontPointSize(size_int)
                cursor.setCharFormat(format_)
                return
            format_ = cursor.charFormat()
            format_.setFontPointSize(size_int)
            cursor.setCharFormat(format_)
        except ValueError:
            pass
    
    def set_text_color(self, color):
        """
        设置文本颜色
        :param color: QColor对象
        """
        # 应用到选中文本
        cursor = self.textCursor()
        format_ = cursor.charFormat()
        format_.setForeground(color)
        cursor.setCharFormat(format_)
    
    def set_alignment(self, alignment):
        """
        设置文本对齐方式
        :param alignment: 对齐方式 (Qt.AlignLeft, Qt.AlignCenter, Qt.AlignRight)
        """
        cursor = self.textCursor()
        block_format = cursor.blockFormat()
        block_format.setAlignment(alignment)
        
        # 如果有选中内容，应用到选中的所有段落
        if cursor.hasSelection():
            # 保存当前选择
            selection_start = cursor.selectionStart()
            selection_end = cursor.selectionEnd()
            
            # 移动到选择的开始位置
            cursor.setPosition(selection_start)
            cursor.movePosition(QTextCursor.StartOfBlock)
            
            # 逐个应用到每个段落
            while cursor.position() < selection_end:
                block_cursor = QTextCursor(cursor.block())
                block_cursor.setBlockFormat(block_format)
                
                # 移动到下一段落
                if not cursor.movePosition(QTextCursor.NextBlock):
                    break
        else:
            # 如果没有选中内容，只应用到当前段落
            cursor.select(QTextCursor.BlockUnderCursor)
            cursor.setBlockFormat(block_format)
    
    def set_first_line_indent(self, indent_type):
        """
        设置首行缩进
        :param indent_type: 缩进类型 ("无缩进", "2字符", "4字符")
        """
        cursor = self.textCursor()
        block_format = cursor.blockFormat()
        
        # 根据选择设置缩进值
        if indent_type == "2字符":
            indent = 2 * self.fontMetrics().width(' ')
        elif indent_type == "4字符":
            indent = 4 * self.fontMetrics().width(' ')
        else:
            indent = 0
            
        block_format.setTextIndent(indent)
        
        # 如果有选中内容，应用到选中的所有段落
        if cursor.hasSelection():
            # 保存当前选择
            selection_start = cursor.selectionStart()
            selection_end = cursor.selectionEnd()
            
            # 移动到选择的开始位置
            cursor.setPosition(selection_start)
            cursor.movePosition(QTextCursor.StartOfBlock)
            
            # 逐个应用到每个段落
            while cursor.position() < selection_end:
                block_cursor = QTextCursor(cursor.block())
                block_cursor.setBlockFormat(block_format)
                
                # 移动到下一段落
                if not cursor.movePosition(QTextCursor.NextBlock):
                    break
        else:
            # 如果没有选中内容，只应用到当前段落
            cursor.select(QTextCursor.BlockUnderCursor)
            cursor.setBlockFormat(block_format)
    
    def set_line_spacing(self, spacing_type):
        """
        设置行间距
        :param spacing_type: 行间距类型 ("单倍", "1.5倍", "双倍")
        """
        cursor = self.textCursor()
        block_format = QTextBlockFormat()
        
        # 根据选择设置行间距
        if spacing_type == "1.5倍":
            block_format.setLineHeight(150, QTextBlockFormat.ProportionalHeight)  # 150% 行高
        elif spacing_type == "双倍":
            block_format.setLineHeight(200, QTextBlockFormat.ProportionalHeight)  # 200% 行高
        else:
            block_format.setLineHeight(100, QTextBlockFormat.ProportionalHeight)  # 100% 行高 (单倍)
            
        # 如果有选中内容，应用到选中的所有段落
        if cursor.hasSelection():
            # 保存当前选择
            selection_start = cursor.selectionStart()
            selection_end = cursor.selectionEnd()
            
            # 移动到选择的开始位置
            cursor.setPosition(selection_start)
            cursor.movePosition(QTextCursor.StartOfBlock)
            
            # 逐个应用到每个段落
            while cursor.position() <= selection_end:  # 修改为 <= 以确保包含最后一个段落
                block_cursor = QTextCursor(cursor.block())
                block_cursor.mergeBlockFormat(block_format)
                
                # 如果无法移动到下一段落，则退出循环
                if not cursor.movePosition(QTextCursor.NextBlock):
                    break
                
                # 如果下一个段落的位置已经超出选择范围，则退出循环
                if cursor.position() > selection_end:
                    break
        else:
            # 如果没有选中内容，只应用到当前段落
            cursor.setBlockFormat(block_format)
    
    def set_edit_mode(self, mode):
        """
        设置编辑模式
        :param mode: 模式类型 ("普通模式", "Markdown模式", "Word模式")
        """
        self.edit_mode = mode
        # 在这里可以添加不同模式的特殊处理逻辑
        # 例如：Markdown模式可以添加语法高亮等
    
    def get_selected_text(self):
        """
        获取选中的文本
        :return: 选中的文本内容
        """
        return self.textCursor().selectedText()
    
    def insert_text(self, text, at_cursor=True):
        """
        在编辑器中插入文本
        :param text: 要插入的文本
        :param at_cursor: 是否在光标位置插入，否则追加到末尾
        """
        if at_cursor:
            # 在当前光标位置插入
            self.insertPlainText(text)
        else:
            # 追加到末尾
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End)
            cursor.insertText(text)
    
    def clear_all(self):
        """
        清空所有文本内容
        """
        self.clear()
    
    def set_content(self, content):
        """
        设置编辑器内容
        :param content: 文本内容
        """
        self.setPlainText(content)
    
    def get_content(self):
        """
        获取编辑器全部内容
        :return: 编辑器中的全部文本
        """
        return self.toPlainText()
    
    def is_empty(self):
        """
        检查编辑器是否为空
        :return: 是否为空
        """
        return self.toPlainText().strip() == ""
    
    def get_current_format(self):
        """
        获取当前光标位置的文本格式
        :return: 字符格式对象
        """
        cursor = self.textCursor()
        return cursor.charFormat()
    
    def has_bold_format(self):
        """
        检查当前光标位置是否为粗体格式
        :return: 是否为粗体
        """
        char_format = self.get_current_format()
        return char_format.fontWeight() == QFont.Bold
    
    def has_italic_format(self):
        """
        检查当前光标位置是否为斜体格式
        :return: 是否为斜体
        """
        char_format = self.get_current_format()
        return char_format.fontItalic()

    def has_underline_format(self):
        """
        检查当前光标位置是否有下划线格式
        :return: 是否有下划线
        """
        char_format = self.get_current_format()
        return char_format.fontUnderline()
    
    def set_bold(self):
        """
        设置选中文字为粗体
        如果已选中文字是粗体，则取消粗体
        """
        cursor = self.textCursor()
        # 保存选择状态
        has_selection = cursor.hasSelection()
        
        if not has_selection:
            # 如果没有选中文本，将光标移动到当前单词
            cursor.movePosition(QTextCursor.StartOfWord, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
        
        # 获取当前格式并切换粗体状态
        format_ = cursor.charFormat()
        is_bold = format_.fontWeight() == QFont.Bold
        format_.setFontWeight(QFont.Normal if is_bold else QFont.Bold)
        cursor.setCharFormat(format_)
        
        # 如果原来没有选择文本，恢复光标位置
        if not has_selection:
            cursor.clearSelection()
            self.setTextCursor(cursor)

    def apply_theme(self, theme):
        """
        应用主题到文本编辑器
        :param theme: 主题名称 ("light" 或 "dark")
        """
        if theme == "light":
            self.setStyleSheet("""
                QTextEdit {
                    background-color: #ffffff !important;
                    color: #2d3748 !important;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                    padding: 20px;
                    font-size: 16px;
                    line-height: 1.8;
                    selection-background-color: #3182ce;
                    selection-color: #ffffff;
                }
                QTextEdit:focus {
                    border-color: #3182ce;
                    box-shadow: 0 0 0 1px rgba(49, 130, 206, 0.1);
                }
                QScrollBar:vertical {
                    background: #f7fafc;
                    width: 12px;
                    border-radius: 6px;
                    margin: 0;
                }
                QScrollBar::handle:vertical {
                    background: #cbd5e0;
                    border-radius: 6px;
                    min-height: 20px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #a0aec0;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    border: none;
                    background: none;
                }
            """)
        else:  # dark theme
            self.setStyleSheet("""
                QTextEdit {
                    background-color: #1a202c !important;
                    color: #e2e8f0 !important;
                    border: 1px solid #4a5568;
                    border-radius: 8px;
                    padding: 16px;
                    font-size: 14px;
                    line-height: 1.6;
                    selection-background-color: #4299e1;
                    selection-color: #ffffff;
                }
                QTextEdit:focus {
                    border-color: #4299e1;
                    box-shadow: 0 0 0 1px rgba(66, 153, 225, 0.2);
                }
                QScrollBar:vertical {
                    background: #2d3748;
                    width: 10px;
                    border-radius: 5px;
                    margin: 0;
                }
                QScrollBar::handle:vertical {
                    background: #4a5568;
                    border-radius: 5px;
                    min-height: 15px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #718096;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    border: none;
                    background: none;
                }
            """)
    
    def set_italic(self):
        """
        设置选中文字为斜体
        如果已选中文字是斜体，则取消斜体
        """
        cursor = self.textCursor()
        # 保存选择状态
        has_selection = cursor.hasSelection()
        
        if not has_selection:
            # 如果没有选中文本，将光标移动到当前单词
            cursor.movePosition(QTextCursor.StartOfWord, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
        
        # 获取当前格式并切换斜体状态
        format_ = cursor.charFormat()
        is_italic = format_.fontItalic()
        format_.setFontItalic(not is_italic)
        cursor.setCharFormat(format_)

        # 如果原来没有选择文本，恢复光标位置
        if not has_selection:
            cursor.clearSelection()
            self.setTextCursor(cursor)

    def apply_theme(self, theme):
        """
        应用主题到文本编辑器
        :param theme: 主题名称 ("light" 或 "dark")
        """
        if theme == "light":
            self.setStyleSheet("""
                QTextEdit {
                    background-color: #ffffff !important;
                    color: #2d3748 !important;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                    padding: 20px;
                    font-size: 16px;
                    line-height: 1.8;
                    selection-background-color: #3182ce;
                    selection-color: #ffffff;
                }
                QTextEdit:focus {
                    border-color: #3182ce;
                    box-shadow: 0 0 0 1px rgba(49, 130, 206, 0.1);
                }
                QScrollBar:vertical {
                    background: #f7fafc;
                    width: 12px;
                    border-radius: 6px;
                    margin: 0;
                }
                QScrollBar::handle:vertical {
                    background: #cbd5e0;
                    border-radius: 6px;
                    min-height: 20px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #a0aec0;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    border: none;
                    background: none;
                }
            """)
        else:  # dark theme
            self.setStyleSheet("""
                QTextEdit {
                    background-color: #1a202c !important;
                    color: #e2e8f0 !important;
                    border: 1px solid #4a5568;
                    border-radius: 8px;
                    padding: 16px;
                    font-size: 14px;
                    line-height: 1.6;
                    selection-background-color: #4299e1;
                    selection-color: #ffffff;
                }
                QTextEdit:focus {
                    border-color: #4299e1;
                    box-shadow: 0 0 0 1px rgba(66, 153, 225, 0.2);
                }
                QScrollBar:vertical {
                    background: #2d3748;
                    width: 10px;
                    border-radius: 5px;
                    margin: 0;
                }
                QScrollBar::handle:vertical {
                    background: #4a5568;
                    border-radius: 5px;
                    min-height: 15px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #718096;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    border: none;
                    background: none;
                }
            """)

    def set_underline(self):
        """
        设置选中文字为下划线
        如果已选中文字有下划线，则取消下划线
        """
        cursor = self.textCursor()
        # 保存选择状态
        has_selection = cursor.hasSelection()

        if not has_selection:
            # 如果没有选中文本，将光标移动到当前单词
            cursor.movePosition(QTextCursor.StartOfWord, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)

        # 获取当前格式并切换下划线状态
        format_ = cursor.charFormat()
        is_underline = format_.fontUnderline()
        format_.setFontUnderline(not is_underline)
        cursor.setCharFormat(format_)

        # 如果原来没有选择文本，恢复光标位置
        if not has_selection:
            cursor.clearSelection()
            self.setTextCursor(cursor)

    def apply_theme(self, theme):
        """
        应用主题到文本编辑器
        :param theme: 主题名称 ("light" 或 "dark")
        """
        if theme == "light":
            self.setStyleSheet("""
                QTextEdit {
                    background-color: #ffffff !important;
                    color: #2d3748 !important;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                    padding: 20px;
                    font-size: 16px;
                    line-height: 1.8;
                    selection-background-color: #3182ce;
                    selection-color: #ffffff;
                }
                QTextEdit:focus {
                    border-color: #3182ce;
                    box-shadow: 0 0 0 1px rgba(49, 130, 206, 0.1);
                }
                QScrollBar:vertical {
                    background: #f7fafc;
                    width: 12px;
                    border-radius: 6px;
                    margin: 0;
                }
                QScrollBar::handle:vertical {
                    background: #cbd5e0;
                    border-radius: 6px;
                    min-height: 20px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #a0aec0;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    border: none;
                    background: none;
                }
            """)
        else:  # dark theme
            self.setStyleSheet("""
                QTextEdit {
                    background-color: #1a202c !important;
                    color: #e2e8f0 !important;
                    border: 1px solid #4a5568;
                    border-radius: 8px;
                    padding: 16px;
                    font-size: 14px;
                    line-height: 1.6;
                    selection-background-color: #4299e1;
                    selection-color: #ffffff;
                }
                QTextEdit:focus {
                    border-color: #4299e1;
                    box-shadow: 0 0 0 1px rgba(66, 153, 225, 0.2);
                }
                QScrollBar:vertical {
                    background: #2d3748;
                    width: 10px;
                    border-radius: 5px;
                    margin: 0;
                }
                QScrollBar::handle:vertical {
                    background: #4a5568;
                    border-radius: 5px;
                    min-height: 15px;
                }
                QScrollBar::handle:vertical:hover {
                    background: #718096;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    border: none;
                    background: none;
                }
            """)