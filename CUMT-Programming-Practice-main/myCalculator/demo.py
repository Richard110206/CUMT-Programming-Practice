#!/usr/bin/env python3
"""
myCalculator 功能演示脚本
展示项目的主要功能
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def demo_basic_calculator():
    """演示基础计算器功能"""
    print("\n" + "="*50)
    print("📊 基础计算器功能演示")
    print("="*50)

    from core.stack_calc.calculator import Calculator

    # 创建计算器实例
    calc = Calculator()

    # 测试各种运算
    expressions = [
        ("4+5", "简单加法"),
        ("5*8+16", "乘加混合运算"),
        ("4*5-6", "乘减混合运算"),
        ("(10+5)*3", "括号运算"),
        ("100/4+5", "除法与加法")
    ]

    for expr, desc in expressions:
        calc.expression = expr
        result = calc.calculate()
        print(f"{expr} = {result}  ({desc})")

    print("✓ 基础计算器基于栈数据结构实现，支持运算符优先级")

def demo_math_functions():
    """演示数学函数功能"""
    print("\n" + "="*50)
    print("🔢 数学函数功能演示")
    print("="*50)

    from core.math_ext.math_functions import MathFunctions

    functions = [
        ("sqrt(16)", MathFunctions.sqrt, [16], "平方根"),
        ("power(2,8)", MathFunctions.power, [2, 8], "幂运算"),
        ("factorial(5)", MathFunctions.factorial, [5], "阶乘"),
        ("reciprocal(4)", MathFunctions.reciprocal, [4], "倒数"),
        ("modulus(17,5)", MathFunctions.modulus, [17, 5], "取模"),
        ("sin(30°)", MathFunctions.sine, [30], "正弦函数"),
        ("cos(60°)", MathFunctions.cosine, [60], "余弦函数"),
        ("log10(1000)", MathFunctions.logarithm, [1000, 10], "常用对数")
    ]

    for expr, func, args, desc in functions:
        try:
            result = func(*args)
            print(f"{expr} = {result:.4f}  ({desc})")
        except Exception as e:
            print(f"{expr} 计算错误: {e}")

    print("✓ 提供丰富的数学函数，包括基础扩展和可选扩展功能")

def demo_number_conversion():
    """演示进制转换功能"""
    print("\n" + "="*50)
    print("🔄 进制转换功能演示")
    print("="*50)

    from convert.number_system.converter import NumberSystemConverter

    # 测试数据
    test_cases = [
        (10, "十进制"),
        (255, "十进制"),
        (1024, "十进制"),
        ("1010", "二进制"),
        ("FF", "十六进制"),
        ("377", "八进制")
    ]

    for value, source_type in test_cases:
        print(f"\n{source_type} {value} 的转换:")

        try:
            # 尝试转换为十进制
            if source_type == "十进制":
                decimal_val = float(value)
            elif source_type == "二进制":
                decimal_val = NumberSystemConverter.binary_to_decimal(value)
            elif source_type == "十六进制":
                decimal_val = NumberSystemConverter.hexadecimal_to_decimal(value)
            elif source_type == "八进制":
                decimal_val = NumberSystemConverter.octal_to_decimal(value)

            binary = NumberSystemConverter.decimal_to_binary(decimal_val)
            octal = NumberSystemConverter.decimal_to_octal(decimal_val)
            hex_val = NumberSystemConverter.decimal_to_hexadecimal(decimal_val)

            print(f"  二进制: {binary}")
            print(f"  八进制: {octal}")
            print(f"  十进制: {decimal_val}")
            print(f"  十六进制: {hex_val}")

        except Exception as e:
            print(f"  转换错误: {e}")

    print("✓ 支持二进制、八进制、十进制、十六进制之间的相互转换")

def demo_length_conversion():
    """演示长度转换功能"""
    print("\n" + "="*50)
    print("📏 长度转换功能演示")
    print("="*50)

    from convert.length.converter import LengthConverter

    conversions = [
        (1, "foot", "meter"),
        (12, "inch", "meter"),
        (1, "meter", "foot"),
        (1, "meter", "inch"),
        (6, "foot", "inch"),
        (1, "foot", "meter", 6)  # 1英尺6英寸转米
    ]

    for value, from_unit, to_unit, *extra in conversions:
        try:
            if extra:
                result = LengthConverter.foot_to_meter(value, extra[0])
                print(f"{value}英尺{extra[0]}英寸 = {result:.4f}米")
            else:
                result = LengthConverter.convert(value, from_unit, to_unit)
                print(f"{value} {from_unit} = {result}")
        except Exception as e:
            print(f"转换错误: {e}")

    print("\n标准换算公式:")
    info = LengthConverter.get_conversion_info()
    for key, value in info.items():
        print(f"  {key} = {value}")

def demo_currency_conversion():
    """演示货币转换功能"""
    print("\n" + "="*50)
    print("💱 货币转换功能演示")
    print("="*50)

    from convert.currency.converter import CurrencyConverter

    converter = CurrencyConverter()

    # 获取支持的货币
    currencies = converter.get_supported_currencies()
    print("支持的货币:")
    for code, info in currencies.items():
        print(f"  {code}: {info['name']} ({info['symbol']})")

    # 演示转换（模拟，不需要网络）
    print(f"\n货币转换演示:")
    test_conversions = [
        (100, "CNY", "USD"),
        (50, "USD", "EUR"),
        (1000, "JPY", "CNY")
    ]

    for amount, from_cur, to_cur in test_conversions:
        try:
            result = converter.convert_currency(amount, from_cur, to_cur)
            if result['success']:
                formatted = converter.format_result(result)
                print(f"  {formatted}")
            else:
                print(f"  {amount} {from_cur} → {to_cur}: 转换失败 - {result['error']}")
        except Exception as e:
            print(f"  {amount} {from_cur} → {to_cur}: 错误 - {e}")

    print("✓ 实时汇率API集成，支持主流货币转换")

def demo_loan_calculator():
    """演示贷款计算器功能"""
    print("\n" + "="*50)
    print("🏠 贷款计算器功能演示")
    print("="*50)

    from domain.loan_calc.calculator import LoanCalculator

    calc = LoanCalculator()

    # 设置贷款参数
    principal = 100000
    annual_rate = 5.5
    loan_term = 30

    print(f"贷款参数:")
    print(f"  贷款本金: ¥{principal:,}")
    print(f"  年利率: {annual_rate}%")
    print(f"  贷款期限: {loan_term}年")

    # 比较两种还款方式
    calc.set_loan_parameters(principal, annual_rate, loan_term, 'years')
    comparison = calc.compare_methods()

    print(f"\n还款方式比较:")

    # 等额本息
    equal = comparison['equal_payment']
    print(f"\n{equal['method']}:")
    print(f"  月还款额: ¥{equal['monthly_payment']:,.2f}")
    print(f"  总还款额: ¥{equal['total_payment']:,.2f}")
    print(f"  总利息: ¥{equal['total_interest']:,.2f}")

    # 等额本金
    equal_principal = comparison['equal_principal']
    print(f"\n{equal_principal['method']}:")
    print(f"  首月还款: ¥{equal_principal['first_month_payment']:,.2f}")
    print(f"  末月还款: ¥{equal_principal['last_month_payment']:,.2f}")
    print(f"  总还款额: ¥{equal_principal['total_payment']:,.2f}")
    print(f"  总利息: ¥{equal_principal['total_interest']:,.2f}")

    print(f"\n利息差额: ¥{comparison['interest_difference']:,.2f}")
    print(f"推荐: {comparison['recommendation']}")

    print("✓ 支持等额本息和等额本金两种还款方式，提供详细还款计划")

def show_project_structure():
    """展示项目结构"""
    print("\n" + "="*50)
    print("📁 项目结构")
    print("="*50)

    print("myCalculator/")
    print("├── core/                      # 核心计算模块")
    print("│   ├── stack_calc/           # 栈实现的四则运算")
    print("│   └── math_ext/             # 数学扩展功能")
    print("├── convert/                   # 换算模块")
    print("│   ├── number_system/        # 进制换算")
    print("│   ├── length/               # 长度换算")
    print("│   └── currency/             # 货币换算")
    print("├── domain/                    # 领域扩展模块")
    print("│   └── loan_calc/            # 贷款计算器")
    print("├── ui/                        # 用户界面")
    print("├── utils/                     # 工具类")
    print("└── main/                      # 程序入口")

    print("\n✓ 模块化设计，结构清晰，便于维护和扩展")

def main():
    """主演示函数"""
    print("🎯 myCalculator 多功能计算器项目演示")
    print("="*60)
    print("这是一个功能完整的Python计算器项目")
    print("采用模块化架构，支持多种计算和转换功能")

    # 展示项目结构
    show_project_structure()

    # 演示各个功能
    demo_basic_calculator()
    demo_math_functions()
    demo_number_conversion()
    demo_length_conversion()
    demo_currency_conversion()
    demo_loan_calculator()

    print("\n" + "="*60)
    print("🚀 项目特色:")
    print("• 基于栈数据结构实现四则运算")
    print("• 丰富的数学函数扩展")
    print("• 实时汇率API集成")
    print("• 专业的贷款计算器")
    print("• 用户友好的图形界面")
    print("• 完善的错误处理")
    print("="*60)

    print("\n💡 启动图形界面:")
    print("python main/main.py")
    print("\n🧪 运行功能测试:")
    print("python test_project.py")

if __name__ == "__main__":
    main()