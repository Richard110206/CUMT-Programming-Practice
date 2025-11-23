"""
栈数据结构的实现
用于计算器中的表达式求值
"""

class Stack:
    """栈数据结构"""

    def __init__(self):
        """初始化空栈"""
        self.items = []

    def is_empty(self):
        """检查栈是否为空"""
        return len(self.items) == 0

    def push(self, item):
        """元素入栈"""
        self.items.append(item)

    def pop(self):
        """元素出栈"""
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError("栈为空，无法执行pop操作")

    def peek(self):
        """查看栈顶元素，但不移除"""
        if not self.is_empty():
            return self.items[-1]
        else:
            raise IndexError("栈为空，无法执行peek操作")

    def size(self):
        """获取栈中元素数量"""
        return len(self.items)

    def clear(self):
        """清空栈"""
        self.items.clear()

    def __str__(self):
        """栈的字符串表示"""
        return str(self.items)