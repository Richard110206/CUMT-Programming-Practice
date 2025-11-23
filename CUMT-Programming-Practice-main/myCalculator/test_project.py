#!/usr/bin/env python3
"""
myCalculator 项目测试脚本
测试所有核心功能是否正常工作
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_stack_functionality():
    """测试栈功能"""
    print("测试栈功能...")
    try:
        from core.stack_calc.stack import Stack
        stack = Stack()

        # 测试基本操作
        assert stack.is_empty() == True
        stack.push(1)
        stack.push(2)
        assert stack.is_empty() == False
        assert stack.peek() == 2
        assert stack.pop() == 2
        assert stack.peek() == 1
        assert stack.size() == 1

        print("  ✓ 栈功能正常")
        return True
    except Exception as e:
        print(f"  ✗ 栈功能测试失败: {e}")
        return False

def test_calculator_functionality():
    """测试计算器功能"""
    print("测试基础计算器功能...")
    try:
        from core.stack_calc.calculator import Calculator
        calc = Calculator()

        # 测试基本运算
        calc.input_digit('4')
        calc.input_operator('+')
        calc.input_digit('5')
        result = calc.calculate()
        assert result == 9

        # 测试连续运算
        calc = Calculator()
        calc.input_digit('5')
        calc.input_operator('*')
        calc.input_digit('8')
        calc.input_operator('+')
        calc.input_digit('16')
        result = calc.calculate()
        assert result == 56

        # 测试复杂表达式
        calc = Calculator()
        calc.input_digit('4')
        calc.input_operator('*')
        calc.input_digit('5')
        calc.input_operator('-')
        calc.input_digit('6')
        result = calc.calculate()
        assert result == 14

        print("  ✓ 基础计算器功能正常")
        return True
    except Exception as e:
        print(f"  ✗ 基础计算器功能测试失败: {e}")
        return False

def test_math_functions():
    """测试数学函数"""
    print("测试数学函数...")
    try:
        from core.math_ext.math_functions import MathFunctions

        # 测试基础函数
        assert MathFunctions.sqrt(16) == 4
        assert abs(MathFunctions.sqrt(2) - 1.41421356) < 0.001

        assert MathFunctions.reciprocal(2) == 0.5
        assert MathFunctions.modulus(10, 3) == 1
        assert MathFunctions.power(2, 3) == 8
        assert MathFunctions.factorial(5) == 120
        assert MathFunctions.absolute(-5) == 5

        # 测试三角函数
        assert abs(MathFunctions.sine(0) - 0) < 0.001
        assert abs(MathFunctions.cosine(0) - 1) < 0.001

        # 测试取整函数
        assert MathFunctions.ceil(3.2) == 4
        assert MathFunctions.floor(3.8) == 3
        assert MathFunctions.round(3.5) == 4

        print("  ✓ 数学函数正常")
        return True
    except Exception as e:
        print(f"  ✗ 数学函数测试失败: {e}")
        return False

def test_number_conversion():
    """测试进制转换"""
    print("测试进制转换...")
    try:
        from convert.number_system.converter import NumberSystemConverter

        # 测试整数转换
        assert NumberSystemConverter.decimal_to_binary(10) == '1010'
        assert NumberSystemConverter.decimal_to_octal(10) == '12'
        assert NumberSystemConverter.decimal_to_hexadecimal(10) == 'A'

        # 测试反向转换
        assert NumberSystemConverter.binary_to_decimal('1010') == 10
        assert NumberSystemConverter.octal_to_decimal('12') == 10
        assert NumberSystemConverter.hexadecimal_to_decimal('A') == 10

        # 测试通用转换
        assert NumberSystemConverter.convert('10', 10, 2) == '1010'
        assert NumberSystemConverter.convert('1010', 2, 10) == '10'

        # 测试小数转换
        binary = NumberSystemConverter.decimal_to_binary(10.5)
        assert '1010.1' in binary

        print("  ✓ 进制转换正常")
        return True
    except Exception as e:
        print(f"  ✗ 进制转换测试失败: {e}")
        return False

def test_length_conversion():
    """测试长度转换"""
    print("测试长度转换...")
    try:
        from convert.length.converter import LengthConverter

        # 测试基本转换
        meters = LengthConverter.foot_to_meter(1)
        assert abs(meters - 0.3048) < 0.001

        inches = LengthConverter.meter_to_inch(0.0254)
        assert abs(inches - 1.0) < 0.001

        # 测试英尺英寸转米
        result = LengthConverter.foot_to_meter(1, 6)
        expected = (1 + 6/12) * 0.3048
        assert abs(result - expected) < 0.001

        # 测试米转英尺英寸
        result = LengthConverter.meter_to_foot(1.8288)
        assert abs(result['total_feet'] - 6.0) < 0.001

        print("  ✓ 长度转换正常")
        return True
    except Exception as e:
        print(f"  ✗ 长度转换测试失败: {e}")
        return False

def test_loan_calculator():
    """测试贷款计算器"""
    print("测试贷款计算器...")
    try:
        from domain.loan_calc.calculator import LoanCalculator
        loan_calc = LoanCalculator()

        # 测试等额本息
        loan_calc.set_loan_parameters(100000, 5.5, 30, 'years')
        loan_calc.set_repayment_method('equal_payment')
        result = loan_calc.calculate()

        assert result['loan_amount'] == 100000
        assert result['annual_rate'] == 5.5
        assert result['loan_term_months'] == 360
        assert 'monthly_payment' in result
        assert result['monthly_payment'] > 0
        assert result['total_payment'] > result['loan_amount']

        # 测试等额本金
        loan_calc.set_repayment_method('equal_principal')
        result = loan_calc.calculate()

        assert 'first_month_payment' in result
        assert 'last_month_payment' in result
        assert result['first_month_payment'] > result['last_month_payment']

        print("  ✓ 贷款计算器正常")
        return True
    except Exception as e:
        print(f"  ✗ 贷款计算器测试失败: {e}")
        return False

def test_ui_imports():
    """测试UI模块导入"""
    print("测试UI模块导入...")
    try:
        # 不实际启动GUI，只测试导入
        import tkinter as tk
        from tkinter import ttk

        # 测试主窗口类可以导入
        import sys
        sys.path.insert(0, project_root)
        from ui.main_window import CalculatorApp

        print("  ✓ UI模块导入正常")
        return True
    except ImportError as e:
        print(f"  ✗ UI模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"  ✗ UI模块测试失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("myCalculator 项目功能测试")
    print("=" * 60)

    tests = [
        test_stack_functionality,
        test_calculator_functionality,
        test_math_functions,
        test_number_conversion,
        test_length_conversion,
        test_loan_calculator,
        test_ui_imports
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  ✗ 测试异常: {e}")
            failed += 1
        print()

    print("=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)

    if failed == 0:
        print("🎉 所有功能测试通过！myCalculator 项目开发完成！")
        return True
    else:
        print("⚠️  部分功能存在问题，请检查相关模块")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)