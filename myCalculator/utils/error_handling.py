"""
自定义异常类模块
定义项目中使用的各种异常类型
"""

class CalculatorError(Exception):
    """计算器基础异常类"""
    pass

class InvalidInputError(CalculatorError):
    """无效输入异常"""
    def __init__(self, message="输入无效"):
        self.message = message
        super().__init__(self.message)

class DivisionByZeroError(CalculatorError):
    """除零异常"""
    def __init__(self, message="除数不能为零"):
        self.message = message
        super().__init__(self.message)

class StackUnderflowError(CalculatorError):
    """栈下溢异常"""
    def __init__(self, message="栈为空，无法执行操作"):
        self.message = message
        super().__init__(self.message)

class ConversionError(CalculatorError):
    """转换错误异常"""
    def __init__(self, message="转换失败"):
        self.message = message
        super().__init__(self.message)

class NetworkError(CalculatorError):
    """网络请求错误异常"""
    def __init__(self, message="网络请求失败"):
        self.message = message
        super().__init__(self.message)

class APIError(CalculatorError):
    """API调用错误异常"""
    def __init__(self, message="API调用失败"):
        self.message = message
        super().__init__(self.message)

class ValidationError(CalculatorError):
    """验证错误异常"""
    def __init__(self, message="数据验证失败"):
        self.message = message
        super().__init__(self.message)

class ParameterError(CalculatorError):
    """参数错误异常"""
    def __init__(self, message="参数设置错误"):
        self.message = message
        super().__init__(self.message)