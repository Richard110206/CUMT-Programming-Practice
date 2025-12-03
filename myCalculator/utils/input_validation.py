"""
数据验证工具模块
提供各种输入验证功能
"""

import re

class InputValidator:
    """输入验证器类"""

    @staticmethod
    def is_number(value):
        """检查是否为有效数字"""
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_positive_number(value):
        """检查是否为正数"""
        try:
            num = float(value)
            return num > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_non_negative_number(value):
        """检查是否为非负数"""
        try:
            num = float(value)
            return num >= 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_integer(value):
        """检查是否为整数"""
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_positive_integer(value):
        """检查是否为正整数"""
        try:
            num = int(value)
            return num > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_non_negative_integer(value):
        """检查是否为非负整数"""
        try:
            num = int(value)
            return num >= 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_valid_percentage(value):
        """检查是否为有效的百分比（0-100）"""
        try:
            num = float(value)
            return 0 <= num <= 100
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_valid_currency_code(code):
        """检查是否为有效的货币代码"""
        if not isinstance(code, str) or len(code) != 3:
            return False
        return code.isalpha() and code.isupper()

    @staticmethod
    def is_valid_number_system(number_str, base):
        """检查数字字符串是否符合指定进制"""
        if base == 2:
            pattern = r'^[01]+(\.[01]+)?$'
        elif base == 8:
            pattern = r'^[0-7]+(\.[0-7]+)?$'
        elif base == 10:
            pattern = r'^\d+(\.\d+)?$'
        elif base == 16:
            pattern = r'^[0-9A-Fa-f]+(\.[0-9A-Fa-f]+)?$'
        else:
            return False

        return bool(re.match(pattern, number_str))

    @staticmethod
    def is_valid_length_unit(unit):
        """检查是否为有效的长度单位"""
        valid_units = ['meter', 'foot', 'inch']
        return unit in valid_units

    @staticmethod
    def is_valid_loan_term(term):
        """检查是否为有效的贷款期限"""
        try:
            num = float(term)
            return num > 0 and num <= 100  # 假设最长100年
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_valid_loan_rate(rate):
        """检查是否为有效的贷款利率"""
        try:
            num = float(rate)
            return 0 <= num <= 50  # 假设最大50%年利率
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_valid_expression(expr):
        """检查是否为有效的数学表达式"""
        if not isinstance(expr, str):
            return False

        # 移除所有空白字符
        expr = expr.replace(" ", "")

        if not expr:
            return False

        # 检查是否包含有效字符
        valid_chars = "0123456789.+-*/()"
        for char in expr:
            if char not in valid_chars:
                return False

        # 简单的括号匹配检查
        stack = []
        for char in expr:
            if char == '(':
                stack.append(char)
            elif char == ')':
                if not stack:
                    return False
                stack.pop()

        return len(stack) == 0

    @staticmethod
    def sanitize_number_input(value):
        """清理和标准化数字输入"""
        if value is None:
            return "0"

        value = str(value).strip()

        # 移除前导零（但保留0和0.xxx）
        if value and value != "0" and not value.startswith("0."):
            while len(value) > 1 and value[0] == '0' and value[1] != '.':
                value = value[1:]

        # 移除末尾的小数点
        if value.endswith('.'):
            value = value[:-1]

        return value if value else "0"

    @staticmethod
    def validate_calculator_input(input_text):
        """验证计算器输入"""
        if not input_text:
            return False

        # 检查是否为数字或运算符
        try:
            # 简单的语法检查
            # 替换运算符以便检查
            test_expr = input_text.replace('×', '*').replace('÷', '/').replace('−', '-')

            # 如果表达式以运算符结尾，则无效
            if test_expr[-1] in '+-*/':
                return False

            return True
        except:
            return False