"""
基于栈的四则运算计算器
支持连续计算和表达式求值
"""

from .stack_handler import Stack

class Calculator:
    """基于栈的计算器类"""

    def __init__(self):
        """初始化计算器"""
        self.expression = ""
        self.result_stack = Stack()
        self.operator_stack = Stack()

    def input_digit(self, digit):
        """输入数字"""
        if isinstance(digit, (int, float)):
            self.expression += str(digit)
        else:
            self.expression += digit

    def input_operator(self, operator):
        """输入运算符"""
        if self.expression and self.expression[-1] in "+-*/":
            # 如果前一个字符也是运算符，替换它
            self.expression = self.expression[:-1] + operator
        else:
            self.expression += operator

    def clear(self):
        """清空当前表达式"""
        self.expression = ""
        self.result_stack.clear()
        self.operator_stack.clear()

    def backspace(self):
        """删除最后一个字符"""
        if self.expression:
            self.expression = self.expression[:-1]

    def get_current_expression(self):
        """获取当前表达式"""
        return self.expression if self.expression else "0"

    def precedence(self, operator):
        """返回运算符优先级"""
        if operator in ('+', '-'):
            return 1
        elif operator in ('*', '/'):
            return 2
        return 0

    def is_operator(self, char):
        """检查字符是否是运算符"""
        return char in '+-*/'

    def apply_operator(self, operator, b, a):
        """应用运算符进行计算"""
        try:
            if operator == '+':
                return a + b
            elif operator == '-':
                return a - b
            elif operator == '*':
                return a * b
            elif operator == '/':
                if b == 0:
                    raise ValueError("除数不能为零")
                return a / b
        except Exception as e:
            raise ValueError(f"计算错误: {str(e)}")

    def calculate(self):
        """计算当前表达式"""
        if not self.expression:
            return 0

        # 清空栈
        self.result_stack.clear()
        self.operator_stack.clear()

        try:
            # 解析表达式中的数字和运算符
            i = 0
            while i < len(self.expression):
                char = self.expression[i]

                if char.isdigit() or char == '.':
                    # 解析数字（可能有多位）
                    num_str = ""
                    while i < len(self.expression) and (self.expression[i].isdigit() or self.expression[i] == '.'):
                        num_str += self.expression[i]
                        i += 1
                    number = float(num_str) if '.' in num_str else int(num_str)
                    self.result_stack.push(number)
                    continue

                elif self.is_operator(char):
                    # 处理运算符优先级
                    while (not self.operator_stack.is_empty() and
                           self.precedence(self.operator_stack.peek()) >= self.precedence(char)):
                        self._calculate_one_operation()
                    self.operator_stack.push(char)

                elif char == '(':
                    self.operator_stack.push(char)

                elif char == ')':
                    # 处理括号
                    while (not self.operator_stack.is_empty() and
                           self.operator_stack.peek() != '('):
                        self._calculate_one_operation()
                    if self.operator_stack.is_empty():
                        raise ValueError("括号不匹配")
                    self.operator_stack.pop()  # 移除 '('

                i += 1

            # 处理剩余的运算符
            while not self.operator_stack.is_empty():
                self._calculate_one_operation()

            if self.result_stack.size() == 1:
                result = self.result_stack.pop()
                # 如果结果是整数，转换为int
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                return result
            else:
                raise ValueError("表达式格式错误")

        except Exception as e:
            self.clear()
            raise ValueError(f"计算错误: {str(e)}")

    def _calculate_one_operation(self):
        """执行一次运算"""
        if self.operator_stack.is_empty():
            raise ValueError("运算符栈为空")

        if self.result_stack.size() < 2:
            raise ValueError("数字栈中没有足够的操作数")

        operator = self.operator_stack.pop()
        b = self.result_stack.pop()
        a = self.result_stack.pop()
        result = self.apply_operator(operator, b, a)
        self.result_stack.push(result)

    def calculate_continuous(self, expression):
        """连续计算功能，支持复杂的表达式计算"""
        old_expression = self.expression
        try:
            self.expression = expression
            result = self.calculate()
            return result
        finally:
            self.expression = old_expression

    def __str__(self):
        """返回当前表达式的字符串表示"""
        return f"Calculator(expression='{self.expression}')"