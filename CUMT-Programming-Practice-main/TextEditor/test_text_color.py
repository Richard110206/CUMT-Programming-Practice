#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文本编辑器颜色修复
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt

def test_text_color():
    app = QApplication(sys.argv)

    window = QWidget()
    layout = QVBoxLayout(window)

    # 测试文本编辑器的颜色设置
    text_edit = QTextEdit()
    text_edit.setPlaceholderText("这里应该能看到黑色文字在白色背景上...")
    text_edit.setStyleSheet("""
        QTextEdit {
            background-color: white !important;
            color: #000000 !important;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 20px;
            font-size: 16px;
            line-height: 1.8;
        }
    """)

    # 添加一些测试文本
    text_edit.setPlainText("这是测试文本\n如果你能看到这段文字，说明颜色设置正确！\nThis is test text in English too.")

    layout.addWidget(text_edit)
    window.setWindowTitle("文本颜色测试")
    window.setGeometry(100, 100, 500, 300)
    window.show()

    return app.exec_()

if __name__ == "__main__":
    test_text_color()