#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件操作模块
负责文本文件的新建、打开、保存等IO操作
"""

import os
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class FileOperations:
    """
    文件操作类
    负责处理文本文件的新建、打开、保存等操作
    """
    
    def __init__(self, parent=None):
        """
        初始化文件操作类
        :param parent: 父窗口组件，用于显示对话框
        """
        self.parent = parent
        self.current_file_path = None
    
    def new_file(self, editor_widget):
        """
        新建文件
        :param editor_widget: 编辑器组件实例
        :return: 是否成功创建新文件
        """
        # 检查是否需要保存当前文件
        if hasattr(editor_widget, 'document') and editor_widget.document().isModified():
            reply = QMessageBox.question(self.parent, "保存", "是否保存当前文件?",
                                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                if not self.save_file(editor_widget):
                    return False
            elif reply == QMessageBox.Cancel:
                return False
        
        # 清空编辑区
        if hasattr(editor_widget, 'clear_all'):
            editor_widget.clear_all()
        else:
            editor_widget.clear()
        
        # 重置当前文件路径
        self.current_file_path = None
        
        # 更新窗口标题
        if self.parent:
            self.parent.setWindowTitle("智能文本编辑器")
        
        return True
    
    def open_file(self, editor_widget):
        """
        打开文件
        :param editor_widget: 编辑器组件实例
        :return: 是否成功打开文件
        """
        # 检查是否需要保存当前文件
        if hasattr(editor_widget, 'document') and editor_widget.document().isModified():
            reply = QMessageBox.question(self.parent, "保存", "是否保存当前文件?",
                                        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                if not self.save_file(editor_widget):
                    return False
            elif reply == QMessageBox.Cancel:
                return False
        
        # 打开文件对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent, 
            "打开文件", 
            "", 
            "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if file_path:
            try:
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # 设置编辑区内容
                if hasattr(editor_widget, 'set_content'):
                    editor_widget.set_content(content)
                else:
                    editor_widget.setPlainText(content)
                
                # 更新当前文件路径
                self.current_file_path = file_path
                
                # 更新窗口标题
                if self.parent:
                    self.parent.setWindowTitle(f"智能文本编辑器 - {os.path.basename(file_path)}")
                
                return True
                
            except UnicodeDecodeError:
                # 尝试使用其他编码
                try:
                    with open(file_path, 'r', encoding='gbk') as file:
                        content = file.read()
                    if hasattr(editor_widget, 'set_content'):
                        editor_widget.set_content(content)
                    else:
                        editor_widget.setPlainText(content)
                    self.current_file_path = file_path
                    if self.parent:
                        self.parent.setWindowTitle(f"智能文本编辑器 - {os.path.basename(file_path)}")
                    return True
                except Exception as e:
                    if self.parent:
                        QMessageBox.warning(self.parent, "错误", f"无法打开文件: {str(e)}")
                    return False
            except Exception as e:
                if self.parent:
                    QMessageBox.warning(self.parent, "错误", f"无法打开文件: {str(e)}")
                return False
        
        return False
    
    def save_file(self, editor_widget, file_path=None):
        """
        保存文件
        :param editor_widget: 编辑器组件实例
        :param file_path: 指定文件路径，如果为None则使用current_file_path
        :return: 是否成功保存文件
        """
        target_path = file_path or self.current_file_path
        if target_path:
            try:
                # 获取编辑器内容
                if hasattr(editor_widget, 'get_content'):
                    content = editor_widget.get_content()
                else:
                    content = editor_widget.toPlainText()

                # 写入文件
                with open(target_path, 'w', encoding='utf-8') as file:
                    file.write(content)

                # 更新当前文件路径（只有当没有指定file_path时）
                if file_path is None:
                    self.current_file_path = target_path

                # 标记文档为未修改
                if hasattr(editor_widget, 'document'):
                    editor_widget.document().setModified(False)
                
                return True
                
            except Exception as e:
                if self.parent:
                    QMessageBox.warning(self.parent, "错误", f"无法保存文件: {str(e)}")
                return False
        else:
            return self.save_file_as(editor_widget)
    
    def save_file_as(self, editor_widget):
        """
        另存为文件
        :param editor_widget: 编辑器组件实例
        :return: 是否成功保存文件
        """
        # 打开保存文件对话框
        file_path, _ = QFileDialog.getSaveFileName(
            self.parent, 
            "另存为", 
            "", 
            "文本文件 (*.txt);;所有文件 (*)"
        )
        
        if file_path:
            try:
                # 获取编辑器内容
                if hasattr(editor_widget, 'get_content'):
                    content = editor_widget.get_content()
                else:
                    content = editor_widget.toPlainText()
                
                # 写入文件
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                # 更新当前文件路径
                self.current_file_path = file_path
                
                # 更新窗口标题
                if self.parent:
                    self.parent.setWindowTitle(f"智能文本编辑器 - {os.path.basename(file_path)}")
                
                # 标记文档为未修改
                if hasattr(editor_widget, 'document'):
                    editor_widget.document().setModified(False)
                
                return True
                
            except Exception as e:
                if self.parent:
                    QMessageBox.warning(self.parent, "错误", f"无法保存文件: {str(e)}")
                return False
        
        return False
    
    def get_current_file_path(self):
        """
        获取当前文件路径
        :return: 当前打开的文件路径，如果没有则返回None
        """
        return self.current_file_path
    
    def set_current_file_path(self, file_path):
        """
        设置当前文件路径
        :param file_path: 文件路径
        """
        self.current_file_path = file_path
        # 更新窗口标题
        if self.parent and file_path:
            self.parent.setWindowTitle(f"智能文本编辑器 - {os.path.basename(file_path)}")