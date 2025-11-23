"""
计算器主界面
使用tkinter创建图形用户界面
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import math

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from core.stack_calc.basic_calculator import Calculator
from core.math_ext.advanced_math import MathFunctions
try:
    from convert.number_system.base_converter import NumberSystemConverter
    from convert.length.length_units import LengthConverter
    from convert.currency.exchange_rate import CurrencyConverter
    from domain.loan_calc.loan_calculator import LoanCalculator
    CURRENCY_AVAILABLE = True
except ImportError as e:
    print(f"警告: 某些模块导入失败: {e}")
    CURRENCY_AVAILABLE = False

    # 创建空的占位符类
    class NumberSystemConverter:
        def convert(self, num, from_base, to_base):
            return "模块不可用"

    class LengthConverter:
        def convert(self, value, from_unit, to_unit):
            return "模块不可用"
        def get_conversion_info(self):
            return {"错误": "模块不可用"}

    class CurrencyConverter:
        def get_supported_currencies(self):
            return {"CNY": {"name": "人民币", "symbol": "¥"}}
        def convert_currency(self, amount, from_curr, to_curr):
            return {"success": False, "error": "模块不可用"}
        def format_result(self, result):
            return "模块不可用"
        def clear_cache(self):
            pass

    class LoanCalculator:
        def set_loan_parameters(self, principal, rate, term, unit):
            pass
        def set_repayment_method(self, method):
            pass
        def calculate(self):
            return {"error": "模块不可用"}
        def format_result(self, result):
            return "模块不可用"
        def compare_methods(self):
            return {"error": "模块不可用"}

class CalculatorApp:
    """计算器应用程序主类"""

    def __init__(self):
        """初始化应用程序"""
        self.root = tk.Tk()
        self.root.title("🧮 多功能计算器 - myCalculator")
        # 设置合适的窗口尺寸
        self.root.geometry("610x720")
        self.root.resizable(True, True)

        # 设置窗口居中
        self.center_window()

        # 初始化各个功能模块
        self.calculator = Calculator()
        self.math_functions = MathFunctions()
        self.number_converter = NumberSystemConverter()
        self.length_converter = LengthConverter()
        self.currency_converter = CurrencyConverter()
        self.loan_calculator = LoanCalculator()

        # 当前计算器状态
        self.current_display = "0"
        self.new_number = True

        # 创建界面
        self.create_widgets()
        self.create_menu()

        # 设置主题
        self.setup_theme()

        # 调试：绑定标签页切换事件
        self.setup_debug_events()

    def center_window(self):
        """窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建标签页控件
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # 创建各个功能页面
        self.create_basic_calculator_tab()
        self.create_math_functions_tab()
        self.create_number_system_tab()
        self.create_length_converter_tab()
        self.create_currency_converter_tab()
        self.create_loan_calculator_tab()

    def create_basic_calculator_tab(self):
        """创建基础计算器页面 - 优化布局"""
        basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(basic_frame, text="🧮 基础计算")

        # 显示屏 - 美化样式，更紧凑
        display_frame = ttk.Frame(basic_frame)
        display_frame.pack(fill=tk.X, padx=12, pady=(12, 8))

        self.display_var = tk.StringVar(value="0")
        self.display = ttk.Label(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 24, "bold"),
            anchor="e",
            relief="solid",
            padding=15,
            background="#1a1a1a",
            foreground="#00ff41"
        )
        self.display.pack(fill=tk.X)

        # 按钮框架 - 更紧凑的布局
        button_frame = ttk.Frame(basic_frame)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

        # 重新设计的按钮布局 - 优化尺寸和间距
        buttons = [
            ('C', 0, 0, 1, 1), ('±', 0, 1, 1, 1), ('%', 0, 2, 1, 1), ('÷', 0, 3, 1, 1),
            ('7', 1, 0, 1, 1), ('8', 1, 1, 1, 1), ('9', 1, 2, 1, 1), ('×', 1, 3, 1, 1),
            ('4', 2, 0, 1, 1), ('5', 2, 1, 1, 1), ('6', 2, 2, 1, 1), ('−', 2, 3, 1, 1),
            ('1', 3, 0, 1, 1), ('2', 3, 1, 1, 1), ('3', 3, 2, 1, 1), ('+', 3, 3, 1, 1),
            ('0', 4, 0, 1, 2), ('.', 4, 2, 1, 1), ('⌫', 4, 3, 1, 1), ('=', 5, 0, 1, 4)
        ]

        for text, row, col, rowspan, colspan in buttons:
            # 根据按钮类型设置不同的颜色
            btn_style = "Number.TButton"
            if text in ['C', '±', '%', '⌫']:
                btn_style = "Function.TButton"
            elif text in ['÷', '×', '−', '+']:
                btn_style = "Operator.TButton"
            elif text == '=':
                btn_style = "Equals.TButton"

            btn = ttk.Button(
                button_frame,
                text=text,
                command=lambda t=text: self.on_basic_button_click(t),
                style=btn_style,
                width=8 if colspan == 1 else 17  # 根据列跨度设置宽度
            )
            btn.grid(row=row, column=col, rowspan=rowspan, columnspan=colspan,
                    sticky="nsew", padx=2, pady=2)

        # 配置网格权重 - 更均匀的分布
        for i in range(6):
            button_frame.grid_rowconfigure(i, weight=1, uniform="row")
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1, uniform="col")

    def create_math_functions_tab(self):
        """创建数学函数页面 - 优化布局"""
        math_frame = ttk.Frame(self.notebook)
        self.notebook.add(math_frame, text="📊 数学函数")

        # 设置字体样式
        large_font = ("Arial", 14, "bold")
        entry_font = ("Arial", 13)

        # 输入框和结果显示 - 使用更大的字体和间距
        input_frame = ttk.LabelFrame(math_frame, text="📝 输入参数与计算结果", padding=15)
        input_frame.pack(fill=tk.X, padx=15, pady=15)

        ttk.Label(input_frame, text="主数值 X:", font=large_font).grid(row=0, column=0, sticky="w", padx=10, pady=12)
        self.math_input_var = tk.StringVar()
        entry1 = ttk.Entry(input_frame, textvariable=self.math_input_var, width=20, font=entry_font)
        entry1.grid(row=0, column=1, padx=10, pady=12, sticky="ew")

        ttk.Label(input_frame, text="第二数值 Y:", font=large_font).grid(row=0, column=2, sticky="w", padx=10, pady=12)
        self.math_input2_var = tk.StringVar()
        entry2 = ttk.Entry(input_frame, textvariable=self.math_input2_var, width=20, font=entry_font)
        entry2.grid(row=0, column=3, padx=10, pady=12, sticky="ew")

        ttk.Label(input_frame, text="计算结果:", font=large_font).grid(row=1, column=0, sticky="w", padx=10, pady=12)
        self.math_result_var = tk.StringVar()
        result_entry = ttk.Entry(input_frame, textvariable=self.math_result_var, width=50, state="readonly", font=entry_font)
        result_entry.grid(row=1, column=1, columnspan=3, padx=10, pady=12, sticky="ew")

        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)

        # 数学函数按钮 - 分类组织，使用更大的字体
        functions_frame = ttk.Frame(math_frame)
        functions_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # 基础运算
        basic_frame = ttk.LabelFrame(functions_frame, text="🔢 基础运算", padding=12)
        basic_frame.pack(fill=tk.X, pady=(0, 15))

        basic_functions = [
            ("√ 平方根", lambda: self.calculate_math("sqrt")),
            ("x^y 幂运算", lambda: self.calculate_math("power")),
            ("% 取模运算", lambda: self.calculate_math("modulus")),
            ("1/x 倒数", lambda: self.calculate_math("reciprocal"))
        ]

        for i, (text, command) in enumerate(basic_functions):
            btn = ttk.Button(basic_frame, text=text, command=command, width=14,
                           style="Number.TButton")
            btn.grid(row=i//2, column=i%2, sticky="ew", padx=8, pady=8)

        basic_frame.grid_columnconfigure(0, weight=1)
        basic_frame.grid_columnconfigure(1, weight=1)

        # 高级函数
        advanced_frame = ttk.LabelFrame(functions_frame, text="🔧 高级函数", padding=12)
        advanced_frame.pack(fill=tk.X, pady=(0, 15))

        advanced_functions = [
            ("n! 阶乘", lambda: self.calculate_math("factorial")),
            ("|x| 绝对值", lambda: self.calculate_math("absolute")),
            ("⌈x⌉ 向上取整", lambda: self.calculate_math("ceil")),
            ("⌊x⌋ 向下取整", lambda: self.calculate_math("floor")),
            ("四舍五入", lambda: self.calculate_math("round"))
        ]

        for i, (text, command) in enumerate(advanced_functions):
            btn = ttk.Button(advanced_frame, text=text, command=command, width=14,
                           style="Function.TButton")
            btn.grid(row=i//3, column=i%3, sticky="ew", padx=6, pady=8)

        for i in range(3):
            advanced_frame.grid_columnconfigure(i, weight=1)

        # 三角函数
        trig_frame = ttk.LabelFrame(functions_frame, text="📐 三角函数", padding=12)
        trig_frame.pack(fill=tk.X)

        trig_functions = [
            ("sin 正弦", lambda: self.calculate_math("sin")),
            ("cos 余弦", lambda: self.calculate_math("cos")),
            ("tan 正切", lambda: self.calculate_math("tan")),
            ("log₁₀ 常用对数", lambda: self.calculate_math("log10")),
            ("ln 自然对数", lambda: self.calculate_math("ln"))
        ]

        for i, (text, command) in enumerate(trig_functions):
            btn = ttk.Button(trig_frame, text=text, command=command, width=14,
                           style="Operator.TButton")
            btn.grid(row=i//3, column=i%3, sticky="ew", padx=6, pady=8)

        for i in range(3):
            trig_frame.grid_columnconfigure(i, weight=1)

    def create_number_system_tab(self):
        """创建进制转换页面"""
        num_frame = ttk.Frame(self.notebook)
        self.notebook.add(num_frame, text="进制转换")

        # 输入框架
        input_frame = ttk.LabelFrame(num_frame, text="🔢 输入数值")
        input_frame.pack(fill=tk.X, padx=15, pady=15)

        # 设置大字体样式
        large_font = ("Arial", 14, "bold")
        entry_font = ("Arial", 16)
        result_font = ("Arial", 15)
        label_font = ("Arial", 12, "bold")

        ttk.Label(input_frame, text="数值:", font=large_font).grid(row=0, column=0, sticky="w", padx=8, pady=10)
        self.num_input_var = tk.StringVar()
        input_entry = ttk.Entry(input_frame, textvariable=self.num_input_var, width=35, font=entry_font)
        input_entry.grid(row=0, column=1, padx=8, pady=10)

        ttk.Label(input_frame, text="源进制:", font=large_font).grid(row=1, column=0, sticky="w", padx=8, pady=10)
        self.num_from_base_var = tk.StringVar(value="10")
        base_combo = ttk.Combobox(input_frame, textvariable=self.num_from_base_var, values=["2", "8", "10", "16"], width=12, font=entry_font)
        base_combo.grid(row=1, column=1, padx=8, pady=10, sticky="w")

        # 转换按钮 - 使用更大的按钮
        convert_btn = ttk.Button(input_frame, text="🔄 转换", command=self.convert_number_system, style="Operator.TButton")
        convert_btn.grid(row=1, column=2, padx=15, pady=10)

        # 结果显示
        result_frame = ttk.LabelFrame(num_frame, text="📋 转换结果")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # 增大结果显示的字体和间距
        result_labels = [
            ("二进制:", "num_binary_var"),
            ("八进制:", "num_octal_var"),
            ("十进制:", "num_decimal_var"),
            ("十六进制:", "num_hex_var")
        ]

        for i, (label_text, var_attr) in enumerate(result_labels):
            ttk.Label(result_frame, text=label_text, font=large_font).grid(row=i, column=0, sticky="w", padx=8, pady=12)

            # 创建变量并设置到实例
            setattr(self, var_attr, tk.StringVar())
            result_entry = ttk.Entry(result_frame, textvariable=getattr(self, var_attr),
                                   state="readonly", font=result_font, width=40)
            result_entry.grid(row=i, column=1, padx=8, pady=12, sticky="ew")

        result_frame.grid_columnconfigure(1, weight=1)

    def create_length_converter_tab(self):
        """创建长度转换页面"""
        length_frame = ttk.Frame(self.notebook)
        self.notebook.add(length_frame, text="长度转换")

        # 设置大字体样式
        large_font = ("Arial", 14, "bold")
        medium_font = ("Arial", 12)
        entry_font = ("Arial", 13)
        result_font = ("Arial", 13, "bold")
        info_font = ("Arial", 11)

        # 单位映射
        unit_mapping = {
            "meter": "米",
            "foot": "英尺",
            "inch": "英寸"
        }

        # 反向映射
        reverse_unit_mapping = {v: k for k, v in unit_mapping.items()}

        # 输入框架 - 使用更大的间距和字体
        input_frame = ttk.LabelFrame(length_frame, text="输入长度", padding=15)
        input_frame.pack(fill=tk.X, padx=15, pady=15)

        # 长度值输入
        ttk.Label(input_frame, text="长度数值:", font=large_font).grid(row=0, column=0, sticky="w", padx=10, pady=12)
        self.length_input_var = tk.StringVar()
        length_entry = ttk.Entry(input_frame, textvariable=self.length_input_var, width=25, font=entry_font)
        length_entry.grid(row=0, column=1, padx=10, pady=12, sticky="ew")

        # 源单位选择
        ttk.Label(input_frame, text="原始单位:", font=large_font).grid(row=1, column=0, sticky="w", padx=10, pady=12)
        self.length_from_var = tk.StringVar(value="米")
        from_units = list(unit_mapping.values())
        from_combo = ttk.Combobox(input_frame, textvariable=self.length_from_var, values=from_units, width=20, font=medium_font)
        from_combo.grid(row=1, column=1, padx=10, pady=12, sticky="ew")

        # 目标单位选择
        ttk.Label(input_frame, text="目标单位:", font=large_font).grid(row=2, column=0, sticky="w", padx=10, pady=12)
        self.length_to_var = tk.StringVar(value="英尺")
        to_units = list(unit_mapping.values())
        to_combo = ttk.Combobox(input_frame, textvariable=self.length_to_var, values=to_units, width=20, font=medium_font)
        to_combo.grid(row=2, column=1, padx=10, pady=12, sticky="ew")

        # 转换按钮 - 使用更大的按钮
        convert_btn = ttk.Button(input_frame, text="🔄 开始转换", command=self.convert_length,
                               style="Operator.TButton", width=20)
        convert_btn.grid(row=3, column=0, columnspan=2, pady=20)

        # 配置列权重
        input_frame.grid_columnconfigure(1, weight=1)

        # 结果显示 - 使用更大的字体和间距
        result_frame = ttk.LabelFrame(length_frame, text="✨ 转换结果", padding=15)
        result_frame.pack(fill=tk.X, padx=15, pady=15)

        self.length_result_var = tk.StringVar(value="请输入长度并点击转换按钮")
        result_label = ttk.Label(result_frame, textvariable=self.length_result_var, font=result_font,
                               foreground="#00ff41", background="#1a1a1a", relief="solid",
                               padding=20, anchor="center")
        result_label.pack(padx=10, pady=15, fill=tk.X)

        # 转换信息 - 使用更大的字体
        info_frame = ttk.LabelFrame(length_frame, text="📏 换算参考信息", padding=15)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # 创建一个更大的文本框
        info_text = tk.Text(info_frame, height=8, width=60, font=info_font,
                           bg="#34495e", fg="white", relief="solid", borderwidth=1)
        info_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # 获取并显示换算信息
        conversion_info = self.length_converter.get_conversion_info()
        for key, value in conversion_info.items():
            info_text.insert(tk.END, f"📌 {key} = {value}\n")
        info_text.config(state="disabled")

        # 存储单位映射供转换函数使用
        self.length_unit_mapping = unit_mapping
        self.length_reverse_unit_mapping = reverse_unit_mapping

    def create_currency_converter_tab(self):
        """创建货币转换页面"""
        currency_frame = ttk.Frame(self.notebook)
        self.notebook.add(currency_frame, text="货币转换")

        # 设置字体样式
        large_font = ("Arial", 14, "bold")
        medium_font = ("Arial", 12)
        entry_font = ("Arial", 13)
        result_font = ("Arial", 13, "bold")
        info_font = ("Arial", 11)

        # 获取货币数据并创建中文映射
        supported_currencies = self.currency_converter.get_supported_currencies()
        currency_mapping = {}
        reverse_currency_mapping = {}

        for code, info in supported_currencies.items():
            chinese_name = info['name']  # 使用中文名称
            currency_mapping[code] = chinese_name
            reverse_currency_mapping[chinese_name] = code

        # 输入框架 - 使用更大的间距
        input_frame = ttk.LabelFrame(currency_frame, text="输入金额", padding=15)
        input_frame.pack(fill=tk.X, padx=15, pady=15)

        # 金额输入
        ttk.Label(input_frame, text="转换金额:", font=large_font).grid(row=0, column=0, sticky="w", padx=10, pady=12)
        self.currency_amount_var = tk.StringVar()
        amount_entry = ttk.Entry(input_frame, textvariable=self.currency_amount_var, width=25, font=entry_font)
        amount_entry.grid(row=0, column=1, padx=10, pady=12, sticky="ew")

        # 源货币选择
        ttk.Label(input_frame, text="原始货币:", font=large_font).grid(row=1, column=0, sticky="w", padx=10, pady=12)
        self.currency_from_var = tk.StringVar(value="人民币")
        from_currencies = list(currency_mapping.values())
        from_combo = ttk.Combobox(input_frame, textvariable=self.currency_from_var,
                                 values=from_currencies, width=20, font=medium_font)
        from_combo.grid(row=1, column=1, padx=10, pady=12, sticky="ew")

        # 目标货币选择
        ttk.Label(input_frame, text="目标货币:", font=large_font).grid(row=2, column=0, sticky="w", padx=10, pady=12)
        self.currency_to_var = tk.StringVar(value="美元")
        to_currencies = list(currency_mapping.values())
        to_combo = ttk.Combobox(input_frame, textvariable=self.currency_to_var,
                               values=to_currencies, width=20, font=medium_font)
        to_combo.grid(row=2, column=1, padx=10, pady=12, sticky="ew")

        # 转换按钮
        convert_btn = ttk.Button(input_frame, text="💱 开始转换", command=self.convert_currency,
                                style="Operator.TButton", width=20)
        convert_btn.grid(row=3, column=0, columnspan=2, pady=20)

        # 配置列权重
        input_frame.grid_columnconfigure(1, weight=1)

        # 结果显示 - 使用更大的字体
        result_frame = ttk.LabelFrame(currency_frame, text="💰 转换结果", padding=15)
        result_frame.pack(fill=tk.X, padx=15, pady=15)

        self.currency_result_var = tk.StringVar(value="请输入金额并点击转换按钮")
        result_label = ttk.Label(result_frame, textvariable=self.currency_result_var, font=result_font,
                                foreground="#00ff41", background="#1a1a1a", relief="solid",
                                padding=15, anchor="center")
        result_label.pack(padx=10, pady=10, fill=tk.X)

        # 汇率信息 - 使用更大的字体
        info_frame = ttk.LabelFrame(currency_frame, text="📈 汇率信息", padding=15)
        info_frame.pack(fill=tk.X, padx=15, pady=15)

        # 汇率显示
        self.currency_rate_var = tk.StringVar()
        rate_label = ttk.Label(info_frame, textvariable=self.currency_rate_var, font=medium_font)
        rate_label.pack(padx=10, pady=8)

        # 缓存状态显示
        self.currency_cache_var = tk.StringVar()
        cache_label = ttk.Label(info_frame, textvariable=self.currency_cache_var, font=info_font)
        cache_label.pack(padx=10, pady=8)

        # 清除缓存按钮
        clear_btn = ttk.Button(info_frame, text="🗑️ 清除缓存", command=self.clear_currency_cache,
                              style="Function.TButton", width=15)
        clear_btn.pack(pady=10)

        # 存储货币映射供转换函数使用
        self.currency_mapping = currency_mapping
        self.reverse_currency_mapping = reverse_currency_mapping

    def create_loan_calculator_tab(self):
        """创建贷款计算器页面"""
        loan_frame = ttk.Frame(self.notebook)
        self.notebook.add(loan_frame, text="贷款计算")

        # 设置字体样式
        large_font = ("Arial", 14, "bold")
        medium_font = ("Arial", 12)
        entry_font = ("Arial", 13)
        result_font = ("Arial", 11)

        # 输入框架 - 使用更大的间距
        input_frame = ttk.LabelFrame(loan_frame, text="🏦 贷款参数设置", padding=15)
        input_frame.pack(fill=tk.X, padx=15, pady=15)

        # 贷款本金
        ttk.Label(input_frame, text="贷款本金 (元):", font=large_font).grid(row=0, column=0, sticky="w", padx=10, pady=12)
        self.loan_principal_var = tk.StringVar(value="100000")
        principal_entry = ttk.Entry(input_frame, textvariable=self.loan_principal_var, width=25, font=entry_font)
        principal_entry.grid(row=0, column=1, padx=10, pady=12, sticky="ew")

        # 年利率
        ttk.Label(input_frame, text="年利率 (%):", font=large_font).grid(row=1, column=0, sticky="w", padx=10, pady=12)
        self.loan_rate_var = tk.StringVar(value="5.5")
        rate_entry = ttk.Entry(input_frame, textvariable=self.loan_rate_var, width=25, font=entry_font)
        rate_entry.grid(row=1, column=1, padx=10, pady=12, sticky="ew")

        # 贷款期限
        ttk.Label(input_frame, text="贷款期限:", font=large_font).grid(row=2, column=0, sticky="w", padx=10, pady=12)

        # 期限数值和单位的组合布局
        term_frame = ttk.Frame(input_frame)
        term_frame.grid(row=2, column=1, padx=10, pady=12, sticky="ew")

        self.loan_term_var = tk.StringVar(value="30")
        term_entry = ttk.Entry(term_frame, textvariable=self.loan_term_var, width=10, font=entry_font)
        term_entry.pack(side=tk.LEFT, padx=(0, 10))

        self.loan_term_unit_var = tk.StringVar(value="年")
        term_units = ["年", "月"]
        term_combo = ttk.Combobox(term_frame, textvariable=self.loan_term_unit_var, values=term_units, width=8, font=medium_font)
        term_combo.pack(side=tk.LEFT)

        # 还款方式
        ttk.Label(input_frame, text="还款方式:", font=large_font).grid(row=3, column=0, sticky="w", padx=10, pady=12)
        method_frame = ttk.Frame(input_frame)
        method_frame.grid(row=3, column=1, columnspan=2, sticky="w", padx=10, pady=12)

        # 使用更大字体的单选按钮
        self.loan_method_var = tk.StringVar(value="equal_payment")
        ttk.Radiobutton(method_frame, text="💰 等额本息", variable=self.loan_method_var,
                       value="equal_payment").pack(side=tk.LEFT, padx=15)
        ttk.Radiobutton(method_frame, text="💳 等额本金", variable=self.loan_method_var,
                       value="equal_principal").pack(side=tk.LEFT, padx=15)

        # 计算按钮区域 - 使用更大的按钮
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)

        calc_btn = ttk.Button(button_frame, text="🧮 计算贷款", command=self.calculate_loan,
                             style="Operator.TButton", width=15)
        calc_btn.pack(side=tk.LEFT, padx=10)

        compare_btn = ttk.Button(button_frame, text="📊 比较两种方式", command=self.compare_loan_methods,
                               style="Function.TButton", width=18)
        compare_btn.pack(side=tk.LEFT, padx=10)

        # 配置列权重
        input_frame.grid_columnconfigure(1, weight=1)

        # 结果显示 - 使用更大的字体
        result_frame = ttk.LabelFrame(loan_frame, text="📋 计算结果详情", padding=15)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # 创建文本框显示结果 - 使用更大的字体
        self.loan_result_text = tk.Text(result_frame, height=18, width=90, font=result_font,
                                       bg="#34495e", fg="white", relief="solid", borderwidth=1,
                                       padx=10, pady=10)
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.loan_result_text.yview)
        self.loan_result_text.configure(yscrollcommand=scrollbar.set)

        # 添加初始提示文本
        initial_text = """🏦 欢迎使用贷款计算器！

请设置贷款参数后点击"计算贷款"按钮查看详细结果。

支持的功能：
• 等额本息还款计算
• 等额本金还款计算
• 两种还款方式对比分析
• 详细的还款计划表

💡 提示：等额本息每月还款额固定，等额本金每月还款额递减。"""

        self.loan_result_text.insert("1.0", initial_text)
        self.loan_result_text.config(state="disabled")

        self.loan_result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="退出", command=self.root.quit)

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)

    def setup_debug_events(self):
        """设置调试事件监听"""
        def on_tab_changed(event):
            try:
                current_tab = self.notebook.index(self.notebook.select())
                tab_text = self.notebook.tab(current_tab, "text")
                print(f"调试: 切换到标签页 {current_tab + 1}: {tab_text}")
            except Exception as e:
                print(f"调试: 标签页切换事件错误: {e}")

        # 绑定标签页切换事件
        self.notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

        # 绑定点击事件
        def on_tab_click(event):
            print(f"调试: 检测到标签页点击事件")

        self.notebook.bind("<Button-1>", on_tab_click)

    def setup_theme(self):
        """设置界面主题 - 深色主题"""
        style = ttk.Style()
        style.theme_use('clam')

        # 设置主窗口背景颜色 - 深色
        self.root.configure(bg='#2c3e50')

        # 数字按钮样式 - 蓝色系
        style.configure("Number.TButton",
                       font=("Arial", 14, "bold"),
                       foreground="white",
                       background="#3498db",
                       borderwidth=0,
                       focuscolor="none",
                       padding=10)
        style.map("Number.TButton",
                 background=[("active", "#2980b9"), ("pressed", "#1e5f8e")])

        # 功能按钮样式 - 橙色系
        style.configure("Function.TButton",
                       font=("Arial", 12, "bold"),
                       foreground="white",
                       background="#e67e22",
                       borderwidth=0,
                       focuscolor="none",
                       padding=10)
        style.map("Function.TButton",
                 background=[("active", "#d35400"), ("pressed", "#a04000")])

        # 运算符按钮样式 - 绿色系
        style.configure("Operator.TButton",
                       font=("Arial", 16, "bold"),
                       foreground="white",
                       background="#27ae60",
                       borderwidth=0,
                       focuscolor="none",
                       padding=10)
        style.map("Operator.TButton",
                 background=[("active", "#229954"), ("pressed", "#1e7e34")])

        # 等于按钮样式 - 红色系
        style.configure("Equals.TButton",
                       font=("Arial", 16, "bold"),
                       foreground="white",
                       background="#e74c3c",
                       borderwidth=0,
                       focuscolor="none",
                       padding=10)
        style.map("Equals.TButton",
                 background=[("active", "#c0392b"), ("pressed", "#a93226")])

        # 默认计算器按钮样式（兼容旧代码）
        style.configure("Calculator.TButton", font=("Arial", 14, "bold"))
        style.configure("Display.TLabel", font=("Arial", 18, "bold"), background="#1a1a1a", foreground="#00ff41")

        # 标签页样式 - 增大字体
        style.configure("TNotebook", background="#34495e", borderwidth=0)
        style.configure("TNotebook.Tab",
                       padding=[16, 12],
                       font=("Arial", 14, "bold"),
                       background="#95a5a6",
                       foreground="white")
        style.map("TNotebook.Tab",
                 background=[("selected", "#3498db"), ("active", "#bdc3c7")])

        # 框架样式 - 深色背景
        style.configure("TFrame", background="#2c3e50")
        style.configure("TLabelframe", background="#2c3e50", foreground="white")
        style.configure("TLabelframe.Label", font=("Arial", 13, "bold"), foreground="white", padding=[8, 6])

        # 标签样式 - 增大所有标签字体
        style.configure("TLabel", background="#2c3e50", foreground="white", font=("Arial", 12))

        # 输入框样式 - 深色主题
        style.configure("TEntry",
                       fieldbackground="#34495e",
                       foreground="white",
                       borderwidth=1,
                       font=("Arial", 11))
        style.map("TEntry",
                 focuscolor=[("focus", "#3498db")])

        # 组合框样式 - 深色主题
        style.configure("TCombobox",
                       fieldbackground="#34495e",
                       foreground="white",
                       borderwidth=1,
                       font=("Arial", 10))
        style.map("TCombobox",
                 focuscolor=[("focus", "#3498db")])

    def on_basic_button_click(self, button_text):
        """处理基础计算器按钮点击"""
        try:
            if button_text == 'C':
                # 清空
                self.calculator.clear()
                self.display_var.set("0")
                self.new_number = True

            elif button_text == '⌫':
                # 退格
                self.calculator.backspace()
                current = self.calculator.get_current_expression()
                self.display_var.set(current)
                if not current or current == "0":
                    self.new_number = True

            elif button_text in '0123456789.':
                # 数字输入
                if self.new_number:
                    self.calculator.clear()
                    self.new_number = False
                self.calculator.input_digit(button_text)
                self.display_var.set(self.calculator.get_current_expression())

            elif button_text in '+−×÷':
                # 运算符输入
                operator = {'−': '-', '×': '*', '÷': '/'}.get(button_text, button_text)
                self.calculator.input_operator(operator)
                self.display_var.set(self.calculator.get_current_expression())
                self.new_number = False

            elif button_text == '=':
                # 计算结果
                result = self.calculator.calculate()
                self.display_var.set(str(result))
                self.new_number = True

            elif button_text == '±':
                # 正负号切换
                current = self.calculator.get_current_expression()
                if current and current != "0":
                    if current.startswith('-'):
                        current = current[1:]
                    else:
                        current = '-' + current
                    self.calculator.expression = current
                    self.display_var.set(current)

            elif button_text == '%':
                # 百分比
                try:
                    current = float(self.calculator.get_current_expression())
                    result = current / 100
                    self.display_var.set(str(result))
                    self.calculator.expression = str(result)
                    self.new_number = True
                except:
                    messagebox.showerror("错误", "无法计算百分比")

        except Exception as e:
            messagebox.showerror("计算错误", str(e))
            self.calculator.clear()
            self.display_var.set("0")
            self.new_number = True

    def calculate_math(self, operation):
        """计算数学函数"""
        try:
            num1 = float(self.math_input_var.get())
            num2 = None

            if operation == "power":
                num2 = float(self.math_input2_var.get())
                result = self.math_functions.power(num1, num2)
            elif operation == "sqrt":
                result = self.math_functions.sqrt(num1)
            elif operation == "modulus":
                num2 = float(self.math_input2_var.get())
                result = self.math_functions.modulus(num1, num2)
            elif operation == "reciprocal":
                result = self.math_functions.reciprocal(num1)
            elif operation == "factorial":
                result = self.math_functions.factorial(num1)
            elif operation == "absolute":
                result = self.math_functions.absolute(num1)
            elif operation == "log10":
                result = self.math_functions.logarithm(num1, 10)
            elif operation == "ln":
                result = self.math_functions.logarithm(num1, math.e)
            elif operation == "sin":
                result = self.math_functions.sine(num1)
            elif operation == "cos":
                result = self.math_functions.cosine(num1)
            elif operation == "tan":
                result = self.math_functions.tangent(num1)
            elif operation == "ceil":
                result = self.math_functions.ceil(num1)
            elif operation == "floor":
                result = self.math_functions.floor(num1)
            elif operation == "round":
                result = self.math_functions.round(num1)
            else:
                raise ValueError("未知操作")

            self.math_result_var.set(str(result))

        except Exception as e:
            messagebox.showerror("计算错误", str(e))

    def convert_number_system(self):
        """进制转换"""
        try:
            number = self.num_input_var.get()
            from_base = int(self.num_from_base_var.get())

            # 转换为所有进制
            decimal_value = self.number_converter.convert(number, from_base, 10)
            binary_value = self.number_converter.convert(decimal_value, 10, 2)
            octal_value = self.number_converter.convert(decimal_value, 10, 8)
            hex_value = self.number_converter.convert(decimal_value, 10, 16)

            self.num_binary_var.set(binary_value)
            self.num_octal_var.set(octal_value)
            self.num_decimal_var.set(decimal_value)
            self.num_hex_var.set(hex_value)

        except Exception as e:
            messagebox.showerror("转换错误", str(e))

    def convert_length(self):
        """长度转换"""
        try:
            value = float(self.length_input_var.get())
            from_unit_chinese = self.length_from_var.get()
            to_unit_chinese = self.length_to_var.get()

            # 将中文单位转换为英文单位供转换函数使用
            from_unit = self.length_reverse_unit_mapping.get(from_unit_chinese, from_unit_chinese)
            to_unit = self.length_reverse_unit_mapping.get(to_unit_chinese, to_unit_chinese)

            # 执行转换
            result = self.length_converter.convert(value, from_unit, to_unit)

            # 格式化结果显示，使用中文单位
            if isinstance(result, str) and "英尺" in result and "英寸" in result:
                # 特殊处理英尺英寸的显示格式
                result_text = f"📏 {value} {from_unit_chinese} = {result}"
            else:
                result_text = f"📏 {value} {from_unit_chinese} = {result} {to_unit_chinese}"

            self.length_result_var.set(result_text)

        except Exception as e:
            messagebox.showerror("转换错误", str(e))

    def convert_currency(self):
        """货币转换"""
        try:
            amount = float(self.currency_amount_var.get())
            from_currency_chinese = self.currency_from_var.get()
            to_currency_chinese = self.currency_to_var.get()

            # 将中文货币名称转换为英文代码供转换函数使用
            from_currency = self.reverse_currency_mapping.get(from_currency_chinese, from_currency_chinese)
            to_currency = self.reverse_currency_mapping.get(to_currency_chinese, to_currency_chinese)

            # 执行转换
            result = self.currency_converter.convert_currency(amount, from_currency, to_currency)

            if result['success']:
                # 格式化结果，使用中文货币名称
                if hasattr(self.currency_converter, 'format_result'):
                    formatted_result = self.currency_converter.format_result(result)
                    # 替换英文货币名称为中文
                    for code, chinese_name in self.currency_mapping.items():
                        formatted_result = formatted_result.replace(code, chinese_name)
                else:
                    # 如果format_result不可用，手动格式化
                    formatted_result = f"💰 {amount:.2f} {from_currency_chinese} = {result['result']:.2f} {to_currency_chinese}"

                self.currency_result_var.set(formatted_result)

                # 显示汇率信息，使用中文货币名称
                rate_text = f"💱 汇率: 1 {from_currency_chinese} = {result['rate']} {to_currency_chinese}"
                self.currency_rate_var.set(rate_text)

                # 显示数据来源
                if result.get('cached'):
                    self.currency_cache_var.set("📦 数据来源: 缓存数据")
                else:
                    timestamp = result.get('timestamp', 'N/A')
                    self.currency_cache_var.set(f"🌐 数据来源: 实时获取 ({timestamp})")
            else:
                messagebox.showerror("转换错误", result['error'])

        except Exception as e:
            messagebox.showerror("转换错误", str(e))

    def clear_currency_cache(self):
        """清除货币汇率缓存"""
        self.currency_converter.clear_cache()
        self.currency_cache_var.set("缓存已清除")

    def calculate_loan(self):
        """计算贷款"""
        try:
            principal = float(self.loan_principal_var.get())
            rate = float(self.loan_rate_var.get())
            term = float(self.loan_term_var.get())
            term_unit_chinese = self.loan_term_unit_var.get()
            method = self.loan_method_var.get()

            # 将中文单位转换为英文供计算函数使用
            term_unit = "years" if term_unit_chinese == "年" else "months"

            self.loan_calculator.set_loan_parameters(principal, rate, term, term_unit)
            self.loan_calculator.set_repayment_method(method)

            result = self.loan_calculator.calculate()
            formatted_result = self.loan_calculator.format_result(result)

            # 显示结果
            self.loan_result_text.config(state="normal")
            self.loan_result_text.delete(1.0, tk.END)

            # 添加美化的标题
            method_name = "等额本息" if method == "equal_payment" else "等额本金"
            title = f"🏦 {method_name}还款计算结果\n"
            title += "=" * 60 + "\n\n"

            self.loan_result_text.insert(tk.END, title)
            self.loan_result_text.insert(tk.END, formatted_result)

            # 如果有还款计划表，也显示出来
            if 'payment_schedule' in result:
                self.loan_result_text.insert(tk.END, "\n\n📊 详细还款计划表\n")
                self.loan_result_text.insert(tk.END, "=" * 60 + "\n")
                self.loan_result_text.insert(tk.END, f"{'期数':<6} {'月还款额':<12} {'本金':<12} {'利息':<12} {'剩余本金':<12}\n")
                self.loan_result_text.insert(tk.END, "-" * 60 + "\n")

                # 只显示前12期和最后3期
                schedule = result['payment_schedule']
                total_months = len(schedule)
                for i, payment in enumerate(schedule):
                    if i < 12 or i >= total_months - 3:
                        month_display = f"{i+1}期" if i < total_months - 3 else f"第{i+1}期(末)"
                        line = f"{month_display:<6} {payment['monthly_payment']:<12} {payment['principal']:<12} {payment['interest']:<12} {payment['remaining_principal']:<12}\n"
                        self.loan_result_text.insert(tk.END, line)

                if total_months > 15:
                    skipped = total_months - 15
                    self.loan_result_text.insert(tk.END, f"... (省略中间 {skipped} 期) ...\n")

            self.loan_result_text.config(state="disabled")

        except Exception as e:
            messagebox.showerror("计算错误", str(e))

    def compare_loan_methods(self):
        """比较两种还款方式"""
        try:
            principal = float(self.loan_principal_var.get())
            rate = float(self.loan_rate_var.get())
            term = float(self.loan_term_var.get())
            term_unit_chinese = self.loan_term_unit_var.get()

            # 将中文单位转换为英文供计算函数使用
            term_unit = "years" if term_unit_chinese == "年" else "months"

            self.loan_calculator.set_loan_parameters(principal, rate, term, term_unit)
            comparison = self.loan_calculator.compare_methods()

            # 显示比较结果
            self.loan_result_text.config(state="normal")
            self.loan_result_text.delete(1.0, tk.END)

            # 添加美化的标题
            title = "📊 两种还款方式详细比较\n"
            title += "=" * 60 + "\n\n"

            self.loan_result_text.insert(tk.END, title)

            # 等额本息
            equal = comparison['equal_payment']
            self.loan_result_text.insert(tk.END, "💰 等额本息还款方式:\n")
            self.loan_result_text.insert(tk.END, "─" * 30 + "\n")
            self.loan_result_text.insert(tk.END, f"  • 月还款额: ¥{equal['monthly_payment']:,.2f}\n")
            self.loan_result_text.insert(tk.END, f"  • 总还款额: ¥{equal['total_payment']:,.2f}\n")
            self.loan_result_text.insert(tk.END, f"  • 总利息: ¥{equal['total_interest']:,.2f}\n\n")

            # 等额本金
            equal_principal = comparison['equal_principal']
            self.loan_result_text.insert(tk.END, "💳 等额本金还款方式:\n")
            self.loan_result_text.insert(tk.END, "─" * 30 + "\n")
            self.loan_result_text.insert(tk.END, f"  • 首月还款: ¥{equal_principal['first_month_payment']:,.2f}\n")
            self.loan_result_text.insert(tk.END, f"  • 末月还款: ¥{equal_principal['last_month_payment']:,.2f}\n")
            self.loan_result_text.insert(tk.END, f"  • 总还款额: ¥{equal_principal['total_payment']:,.2f}\n")
            self.loan_result_text.insert(tk.END, f"  • 总利息: ¥{equal_principal['total_interest']:,.2f}\n\n")

            # 利息差额和推荐
            self.loan_result_text.insert(tk.END, "🔍 对比分析:\n")
            self.loan_result_text.insert(tk.END, "─" * 20 + "\n")
            self.loan_result_text.insert(tk.END, f"  • 利息差额: ¥{comparison['interest_difference']:,.2f}\n")
            self.loan_result_text.insert(tk.END, f"  • 🌟 推荐选择: {comparison['recommendation']}\n\n")

            # 添加小贴士
            self.loan_result_text.insert(tk.END, "💡 小贴士:\n")
            self.loan_result_text.insert(tk.END, "─" * 15 + "\n")
            self.loan_result_text.insert(tk.END, "  • 等额本息：每月还款额固定，便于规划，适合收入稳定人群\n")
            self.loan_result_text.insert(tk.END, "  • 等额本金：前期还款压力大，总利息较少，适合收入较高人群\n")

            self.loan_result_text.config(state="disabled")

        except Exception as e:
            messagebox.showerror("计算错误", str(e))

    def show_about(self):
        """显示关于对话框"""
        about_text = """多功能计算器 - myCalculator

版本: 1.0
作者: 计算机课程设计项目

功能特性:
• 基础四则运算（基于栈实现）
• 扩展数学函数
• 进制转换
• 长度单位转换
• 货币汇率转换（实时API）
• 贷款计算器

项目结构清晰，模块化设计，
支持多种计算和转换功能。"""

        messagebox.showinfo("关于 myCalculator", about_text)

    def run(self):
        """运行应用程序"""
        self.root.mainloop()

def main():
    """主函数"""
    app = CalculatorApp()
    app.run()

if __name__ == "__main__":
    main()