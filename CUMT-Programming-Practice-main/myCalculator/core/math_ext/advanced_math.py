"""
数学扩展功能模块
实现平方根、取模、倒数、幂运算、阶乘等数学功能
"""

import math

class MathFunctions:
    """数学扩展功能类"""

    @staticmethod
    def sqrt(x):
        """计算平方根"""
        try:
            if x < 0:
                raise ValueError("负数不能计算实数平方根")
            result = math.sqrt(x)
            # 如果结果是整数，转换为int
            if isinstance(result, float) and result.is_integer():
                return int(result)
            return result
        except Exception as e:
            raise ValueError(f"平方根计算错误: {str(e)}")

    @staticmethod
    def power(x, y):
        """计算幂运算 x^y"""
        try:
            result = math.pow(x, y)
            # 如果结果是整数，转换为int
            if isinstance(result, float) and result.is_integer():
                return int(result)
            return result
        except Exception as e:
            raise ValueError(f"幂运算错误: {str(e)}")

    @staticmethod
    def modulus(x, y):
        """计算取模运算 x % y"""
        try:
            if y == 0:
                raise ValueError("除数不能为零")
            return x % y
        except Exception as e:
            raise ValueError(f"取模运算错误: {str(e)}")

    @staticmethod
    def reciprocal(x):
        """计算倒数 1/x"""
        try:
            if x == 0:
                raise ValueError("零的倒数不存在")
            result = 1 / x
            # 如果结果是整数，转换为int
            if isinstance(result, float) and result.is_integer():
                return int(result)
            return result
        except Exception as e:
            raise ValueError(f"倒数计算错误: {str(e)}")

    @staticmethod
    def factorial(x):
        """计算阶乘 x!"""
        try:
            if not isinstance(x, int) or x < 0:
                raise ValueError("阶乘只能计算非负整数")
            return math.factorial(x)
        except Exception as e:
            raise ValueError(f"阶乘计算错误: {str(e)}")

    @staticmethod
    def absolute(x):
        """计算绝对值 |x|"""
        return abs(x)

    @staticmethod
    def logarithm(x, base=10):
        """计算对数 log_base(x)，默认常用对数"""
        try:
            if x <= 0:
                raise ValueError("对数的真数必须大于0")
            if base <= 0 or base == 1:
                raise ValueError("对数的底数必须大于0且不等于1")
            if base == 10:
                result = math.log10(x)
            elif base == math.e:
                result = math.log(x)
            else:
                result = math.log(x, base)

            # 如果结果是整数，转换为int
            if isinstance(result, float) and result.is_integer():
                return int(result)
            return result
        except Exception as e:
            raise ValueError(f"对数计算错误: {str(e)}")

    @staticmethod
    def sine(x, degrees=True):
        """计算正弦函数 sin(x)"""
        try:
            if degrees:
                x = math.radians(x)
            result = math.sin(x)
            # 处理浮点数精度问题
            if abs(result) < 1e-10:
                result = 0
            if abs(result - round(result)) < 1e-10:
                return round(result)
            return result
        except Exception as e:
            raise ValueError(f"正弦计算错误: {str(e)}")

    @staticmethod
    def cosine(x, degrees=True):
        """计算余弦函数 cos(x)"""
        try:
            if degrees:
                x = math.radians(x)
            result = math.cos(x)
            # 处理浮点数精度问题
            if abs(result) < 1e-10:
                result = 0
            if abs(result - round(result)) < 1e-10:
                return round(result)
            return result
        except Exception as e:
            raise ValueError(f"余弦计算错误: {str(e)}")

    @staticmethod
    def tangent(x, degrees=True):
        """计算正切函数 tan(x)"""
        try:
            if degrees:
                x = math.radians(x)
            result = math.tan(x)
            # 处理浮点数精度问题和无穷大
            if abs(result) > 1e15:
                raise ValueError("正切函数值超出范围")
            if abs(result) < 1e-10:
                result = 0
            if abs(result - round(result)) < 1e-10:
                return round(result)
            return result
        except Exception as e:
            raise ValueError(f"正切计算错误: {str(e)}")

    @staticmethod
    def floor(x):
        """向下取整"""
        return math.floor(x)

    @staticmethod
    def ceil(x):
        """向上取整"""
        return math.ceil(x)

    @staticmethod
    def round(x, digits=0):
        """四舍五入"""
        if digits == 0:
            return round(x)
        else:
            return round(x, digits)

# 创建全局实例，方便其他模块调用
math_func = MathFunctions()