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
        # 使用系统默认字体族，只设置字号
        default_font = QFont()
        default_font.setPointSize(12)
        self.setFont(default_font)
        # 设置Tab宽度为4个空格
        self.setTabStopWidth(4 * self.fontMetrics().width(' '))
        # 支持自动换行
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        # 支持撤销/重做功能
        self.setUndoRedoEnabled(True)
        
        # 初始化编辑模式
        self.edit_mode = "普通模式"
        
    def set_text_font(self, font_family):
        """
        设置文本字体
        :param font_family: 字体名称
        """
        current_font = self.font()
        current_font.setFamily(font_family)
        self.setFont(current_font)
        # 应用到选中文本
        cursor = self.textCursor()
        if not cursor.hasSelection():
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
            current_font = self.font()
            current_font.setPointSize(size_int)
            self.setFont(current_font)
            # 应用到选中文本
            cursor = self.textCursor()
            if not cursor.hasSelection():
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
        if not cursor.hasSelection():
            return
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
        block_format = cursor.blockFormat()
        
        # 根据选择设置行间距
        if spacing_type == "1.5倍":
            block_format.setLineHeight(1.5, QTextBlockFormat.ProportionalHeight)
        elif spacing_type == "双倍":
            block_format.setLineHeight(2.0, QTextBlockFormat.ProportionalHeight)
        else:
            block_format.setLineHeight(1.0, QTextBlockFormat.ProportionalHeight)
            
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
        
    def set_italic(self):
        """
        设置选中文字为斜体
        如果已选中文字是斜体，则取消斜体
        """
        cursor = self.textCursor()
        if not cursor.hasSelection():
            # 如果没有选中文本，将光标移动到当前单词
            cursor.movePosition(QTextCursor.WordUnderCursor, QTextCursor.SelectCurrentWord)
        
        format_ = cursor.charFormat()
        # 切换斜体状态
        format_.setFontItalic(not format_.fontItalic())
        cursor.setCharFormat(format_)
        self.setTextCursor(cursor)