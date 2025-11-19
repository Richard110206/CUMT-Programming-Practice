#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文本编辑器程序入口
负责初始化应用程序和启动主窗口
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# 导入主窗口类
from main_window import MainWindow


if __name__ == "__main__":
    """
    程序主入口
    """
    # 创建QApplication实例
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("文本编辑器")
    app.setApplicationVersion("1.0")
    
    # 确保中文显示正常
    # 使用系统默认字体以避免字体不存在的问题
    font = app.font()
    app.setFont(font)
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序主循环
    sys.exit(app.exec_())