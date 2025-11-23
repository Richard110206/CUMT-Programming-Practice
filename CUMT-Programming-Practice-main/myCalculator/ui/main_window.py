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

from core.stack_calc.calculator import Calculator
from core.math_ext.math_functions import MathFunctions
from convert.number_system.converter import NumberSystemConverter
from convert.length.converter import LengthConverter
from convert.currency.converter import CurrencyConverter
from domain.loan_calc.calculator import LoanCalculator

class CalculatorApp:
    """计算器应用程序主类"""

    def __init__(self):
        """初始化应用程序"""
        self.root = tk.Tk()
        self.root.title("🧮 多功能计算器 - myCalculator")
        # 修改为垂直长方形布局：窄一些，高一些
        self.root.geometry("500x900")
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

        # 显示屏 - 美化样式
        display_frame = ttk.Frame(basic_frame)
        display_frame.pack(fill=tk.X, padx=15, pady=(15, 10))

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
        button_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

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
                    sticky="nsew", padx=3, pady=3)

        # 配置网格权重 - 更均匀的分布
        for i in range(6):
            button_frame.grid_rowconfigure(i, weight=1, uniform="row")
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1, uniform="col")

    def create_math_functions_tab(self):
        """创建数学函数页面 - 优化布局"""
        math_frame = ttk.Frame(self.notebook)
        self.notebook.add(math_frame, text="📊 数学函数")

        # 输入框和结果显示 - 更紧凑的布局
        input_frame = ttk.LabelFrame(math_frame, text="输入与结果", padding=10)
        input_frame.pack(fill=tk.X, padx=15, pady=(15, 10))

        ttk.Label(input_frame, text="主数值:").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.math_input_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.math_input_var, width=15).grid(row=0, column=1, padx=5, pady=3)

        ttk.Label(input_frame, text="第二数值:").grid(row=0, column=2, sticky="w", padx=5, pady=3)
        self.math_input2_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.math_input2_var, width=15).grid(row=0, column=3, padx=5, pady=3)

        ttk.Label(input_frame, text="计算结果:").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.math_result_var = tk.StringVar()
        result_entry = ttk.Entry(input_frame, textvariable=self.math_result_var, width=35, state="readonly")
        result_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=3, sticky="ew")

        input_frame.grid_columnconfigure(1, weight=1)
        input_frame.grid_columnconfigure(3, weight=1)

        # 数学函数按钮 - 分类组织
        functions_frame = ttk.Frame(math_frame)
        functions_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        # 基础运算
        basic_frame = ttk.LabelFrame(functions_frame, text="基础运算", padding=8)
        basic_frame.pack(fill=tk.X, pady=(0, 10))

        basic_functions = [
            ("平方根 √", lambda: self.calculate_math("sqrt")),
            ("幂运算 x^y", lambda: self.calculate_math("power")),
            ("取模 %", lambda: self.calculate_math("modulus")),
            ("倒数 1/x", lambda: self.calculate_math("reciprocal"))
        ]

        for i, (text, command) in enumerate(basic_functions):
            btn = ttk.Button(basic_frame, text=text, command=command, width=12)
            btn.grid(row=i//2, column=i%2, sticky="ew", padx=4, pady=3)

        basic_frame.grid_columnconfigure(0, weight=1)
        basic_frame.grid_columnconfigure(1, weight=1)

        # 高级函数
        advanced_frame = ttk.LabelFrame(functions_frame, text="高级函数", padding=8)
        advanced_frame.pack(fill=tk.X, pady=(0, 10))

        advanced_functions = [
            ("阶乘 n!", lambda: self.calculate_math("factorial")),
            ("绝对值 |x|", lambda: self.calculate_math("absolute")),
            ("向上取整 ⌈x⌉", lambda: self.calculate_math("ceil")),
            ("向下取整 ⌊x⌋", lambda: self.calculate_math("floor")),
            ("四舍五入", lambda: self.calculate_math("round"))
        ]

        for i, (text, command) in enumerate(advanced_functions):
            btn = ttk.Button(advanced_frame, text=text, command=command, width=12)
            btn.grid(row=i//3, column=i%3, sticky="ew", padx=4, pady=3)

        for i in range(3):
            advanced_frame.grid_columnconfigure(i, weight=1)

        # 三角函数
        trig_frame = ttk.LabelFrame(functions_frame, text="三角函数", padding=8)
        trig_frame.pack(fill=tk.X)

        trig_functions = [
            ("正弦 sin", lambda: self.calculate_math("sin")),
            ("余弦 cos", lambda: self.calculate_math("cos")),
            ("正切 tan", lambda: self.calculate_math("tan")),
            ("常用对数 log₁₀", lambda: self.calculate_math("log10")),
            ("自然对数 ln", lambda: self.calculate_math("ln"))
        ]

        for i, (text, command) in enumerate(trig_functions):
            btn = ttk.Button(trig_frame, text=text, command=command, width=12)
            btn.grid(row=i//3, column=i%3, sticky="ew", padx=4, pady=3)

        for i in range(3):
            trig_frame.grid_columnconfigure(i, weight=1)

    def create_number_system_tab(self):
        """创建进制转换页面"""
        num_frame = ttk.Frame(self.notebook)
        self.notebook.add(num_frame, text="进制转换")

        # 输入框架
        input_frame = ttk.LabelFrame(num_frame, text="输入")
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(input_frame, text="数值:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.num_input_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.num_input_var, width=30).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="源进制:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.num_from_base_var = tk.StringVar(value="10")
        ttk.Combobox(input_frame, textvariable=self.num_from_base_var, values=["2", "8", "10", "16"], width=10).grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(input_frame, text="转换", command=self.convert_number_system).grid(row=0, column=4, padx=5, pady=5)

        # 结果显示
        result_frame = ttk.LabelFrame(num_frame, text="转换结果")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(result_frame, text="二进制:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.num_binary_var = tk.StringVar()
        ttk.Entry(result_frame, textvariable=self.num_binary_var, state="readonly").grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(result_frame, text="八进制:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.num_octal_var = tk.StringVar()
        ttk.Entry(result_frame, textvariable=self.num_octal_var, state="readonly").grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(result_frame, text="十进制:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.num_decimal_var = tk.StringVar()
        ttk.Entry(result_frame, textvariable=self.num_decimal_var, state="readonly").grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(result_frame, text="十六进制:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.num_hex_var = tk.StringVar()
        ttk.Entry(result_frame, textvariable=self.num_hex_var, state="readonly").grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        result_frame.grid_columnconfigure(1, weight=1)

    def create_length_converter_tab(self):
        """创建长度转换页面"""
        length_frame = ttk.Frame(self.notebook)
        self.notebook.add(length_frame, text="长度转换")

        # 输入框架
        input_frame = ttk.Frame(length_frame)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(input_frame, text="长度值:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.length_input_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.length_input_var, width=20).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="源单位:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.length_from_var = tk.StringVar(value="meter")
        ttk.Combobox(input_frame, textvariable=self.length_from_var, values=["meter", "foot", "inch"], width=15).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="目标单位:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.length_to_var = tk.StringVar(value="foot")
        ttk.Combobox(input_frame, textvariable=self.length_to_var, values=["meter", "foot", "inch"], width=15).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text="转换", command=self.convert_length).grid(row=1, column=3, padx=5, pady=5)

        # 结果显示
        result_frame = ttk.LabelFrame(length_frame, text="转换结果")
        result_frame.pack(fill=tk.X, padx=10, pady=10)

        self.length_result_var = tk.StringVar()
        result_label = ttk.Label(result_frame, textvariable=self.length_result_var, font=("Arial", 12))
        result_label.pack(padx=10, pady=10)

        # 转换信息
        info_frame = ttk.LabelFrame(length_frame, text="换算信息")
        info_frame.pack(fill=tk.X, padx=10, pady=10)

        info_text = tk.Text(info_frame, height=6, width=50)
        info_text.pack(padx=10, pady=10)

        conversion_info = self.length_converter.get_conversion_info()
        for key, value in conversion_info.items():
            info_text.insert(tk.END, f"{key} = {value}\n")
        info_text.config(state="disabled")

    def create_currency_converter_tab(self):
        """创建货币转换页面"""
        currency_frame = ttk.Frame(self.notebook)
        self.notebook.add(currency_frame, text="货币转换")

        # 输入框架
        input_frame = ttk.Frame(currency_frame)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(input_frame, text="金额:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.currency_amount_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.currency_amount_var, width=20).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="源货币:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.currency_from_var = tk.StringVar(value="CNY")
        currencies = list(self.currency_converter.get_supported_currencies().keys())
        ttk.Combobox(input_frame, textvariable=self.currency_from_var, values=currencies, width=10).grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="目标货币:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.currency_to_var = tk.StringVar(value="USD")
        ttk.Combobox(input_frame, textvariable=self.currency_to_var, values=currencies, width=10).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(input_frame, text="转换", command=self.convert_currency).grid(row=1, column=3, padx=5, pady=5)

        # 结果显示
        result_frame = ttk.LabelFrame(currency_frame, text="转换结果")
        result_frame.pack(fill=tk.X, padx=10, pady=10)

        self.currency_result_var = tk.StringVar()
        result_label = ttk.Label(result_frame, textvariable=self.currency_result_var, font=("Arial", 12))
        result_label.pack(padx=10, pady=10)

        # 汇率信息
        info_frame = ttk.LabelFrame(currency_frame, text="汇率信息")
        info_frame.pack(fill=tk.X, padx=10, pady=10)

        self.currency_rate_var = tk.StringVar()
        rate_label = ttk.Label(info_frame, textvariable=self.currency_rate_var)
        rate_label.pack(padx=10, pady=5)

        self.currency_cache_var = tk.StringVar()
        cache_label = ttk.Label(info_frame, textvariable=self.currency_cache_var)
        cache_label.pack(padx=10, pady=5)

        ttk.Button(info_frame, text="清除缓存", command=self.clear_currency_cache).pack(pady=5)

    def create_loan_calculator_tab(self):
        """创建贷款计算器页面"""
        loan_frame = ttk.Frame(self.notebook)
        self.notebook.add(loan_frame, text="贷款计算")

        # 输入框架
        input_frame = ttk.LabelFrame(loan_frame, text="贷款参数")
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        # 贷款本金
        ttk.Label(input_frame, text="贷款本金 (元):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.loan_principal_var = tk.StringVar(value="100000")
        ttk.Entry(input_frame, textvariable=self.loan_principal_var, width=20).grid(row=0, column=1, padx=5, pady=5)

        # 年利率
        ttk.Label(input_frame, text="年利率 (%):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.loan_rate_var = tk.StringVar(value="5.5")
        ttk.Entry(input_frame, textvariable=self.loan_rate_var, width=20).grid(row=1, column=1, padx=5, pady=5)

        # 贷款期限
        ttk.Label(input_frame, text="贷款期限:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.loan_term_var = tk.StringVar(value="30")
        ttk.Entry(input_frame, textvariable=self.loan_term_var, width=20).grid(row=2, column=1, padx=5, pady=5)

        self.loan_term_unit_var = tk.StringVar(value="years")
        ttk.Combobox(input_frame, textvariable=self.loan_term_unit_var, values=["years", "months"], width=10).grid(row=2, column=2, padx=5, pady=5)

        # 还款方式
        ttk.Label(input_frame, text="还款方式:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.loan_method_var = tk.StringVar(value="equal_payment")
        method_frame = ttk.Frame(input_frame)
        method_frame.grid(row=3, column=1, columnspan=2, sticky="w", padx=5, pady=5)

        ttk.Radiobutton(method_frame, text="等额本息", variable=self.loan_method_var, value="equal_payment").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(method_frame, text="等额本金", variable=self.loan_method_var, value="equal_principal").pack(side=tk.LEFT, padx=5)

        # 计算按钮
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=10)

        ttk.Button(button_frame, text="计算", command=self.calculate_loan).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="比较两种方式", command=self.compare_loan_methods).pack(side=tk.LEFT, padx=5)

        # 结果显示
        result_frame = ttk.LabelFrame(loan_frame, text="计算结果")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建文本框显示结果
        self.loan_result_text = tk.Text(result_frame, height=20, width=80)
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.loan_result_text.yview)
        self.loan_result_text.configure(yscrollcommand=scrollbar.set)

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

    def setup_theme(self):
        """设置界面主题 - 丰富的颜色方案"""
        style = ttk.Style()
        style.theme_use('clam')

        # 设置主窗口背景颜色
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
        style.configure("Display.TLabel", font=("Arial", 18, "bold"), background="white", foreground="black")

        # 标签页样式
        style.configure("TNotebook", background="#34495e", borderwidth=0)
        style.configure("TNotebook.Tab",
                       padding=[12, 8],
                       font=("Arial", 11, "bold"),
                       background="#95a5a6",
                       foreground="white")
        style.map("TNotebook.Tab",
                 background=[("selected", "#3498db"), ("active", "#bdc3c7")])

        # 框架样式
        style.configure("TFrame", background="#2c3e50")
        style.configure("TLabelframe", background="#2c3e50", foreground="white")
        style.configure("TLabelframe.Label", font=("Arial", 10, "bold"), foreground="white")

        # 标签样式
        style.configure("TLabel", background="#2c3e50", foreground="white", font=("Arial", 10))
        style.configure("TLabelframe.Label", background="#2c3e50", foreground="white", font=("Arial", 11, "bold"))

        # 输入框样式
        style.configure("TEntry",
                       fieldbackground="#ecf0f1",
                       foreground="#2c3e50",
                       borderwidth=1,
                       font=("Arial", 11))
        style.map("TEntry",
                 focuscolor=[("focus", "#3498db")])

        # 组合框样式
        style.configure("TCombobox",
                       fieldbackground="#ecf0f1",
                       foreground="#2c3e50",
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
            from_unit = self.length_from_var.get()
            to_unit = self.length_to_var.get()

            result = self.length_converter.convert(value, from_unit, to_unit)
            self.length_result_var.set(f"{value} {from_unit} = {result}")

        except Exception as e:
            messagebox.showerror("转换错误", str(e))

    def convert_currency(self):
        """货币转换"""
        try:
            amount = float(self.currency_amount_var.get())
            from_currency = self.currency_from_var.get()
            to_currency = self.currency_to_var.get()

            result = self.currency_converter.convert_currency(amount, from_currency, to_currency)

            if result['success']:
                formatted_result = self.currency_converter.format_result(result)
                self.currency_result_var.set(formatted_result)
                self.currency_rate_var.set(f"汇率: 1 {from_currency} = {result['rate']} {to_currency}")

                if result.get('cached'):
                    self.currency_cache_var.set("数据来源: 缓存")
                else:
                    self.currency_cache_var.set(f"数据来源: 实时获取 ({result.get('timestamp', 'N/A')})")
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
            term_unit = self.loan_term_unit_var.get()
            method = self.loan_method_var.get()

            self.loan_calculator.set_loan_parameters(principal, rate, term, term_unit)
            self.loan_calculator.set_repayment_method(method)

            result = self.loan_calculator.calculate()
            formatted_result = self.loan_calculator.format_result(result)

            # 显示结果
            self.loan_result_text.delete(1.0, tk.END)
            self.loan_result_text.insert(tk.END, formatted_result)

            # 如果有还款计划表，也显示出来
            if 'payment_schedule' in result:
                self.loan_result_text.insert(tk.END, "\n\n=== 还款计划表 ===\n")
                self.loan_result_text.insert(tk.END, "期数\t月还款额\t本金\t利息\t剩余本金\n")
                self.loan_result_text.insert(tk.END, "-" * 50 + "\n")

                # 只显示前12期和最后3期
                schedule = result['payment_schedule']
                for i, payment in enumerate(schedule):
                    if i < 12 or i >= len(schedule) - 3:
                        line = f"{payment['month']}\t{payment['monthly_payment']}\t{payment['principal']}\t{payment['interest']}\t{payment['remaining_principal']}\n"
                        self.loan_result_text.insert(tk.END, line)

                if len(schedule) > 15:
                    self.loan_result_text.insert(tk.END, "...\n")

        except Exception as e:
            messagebox.showerror("计算错误", str(e))

    def compare_loan_methods(self):
        """比较两种还款方式"""
        try:
            principal = float(self.loan_principal_var.get())
            rate = float(self.loan_rate_var.get())
            term = float(self.loan_term_var.get())
            term_unit = self.loan_term_unit_var.get()

            self.loan_calculator.set_loan_parameters(principal, rate, term, term_unit)
            comparison = self.loan_calculator.compare_methods()

            # 显示比较结果
            self.loan_result_text.delete(1.0, tk.END)
            self.loan_result_text.insert(tk.END, "=== 还款方式比较 ===\n\n")

            # 等额本息
            equal = comparison['equal_payment']
            self.loan_result_text.insert(tk.END, f"{equal['method']}:\n")
            self.loan_result_text.insert(tk.END, f"  月还款额: ¥{equal['monthly_payment']:,.2f}\n")
            self.loan_result_text.insert(tk.END, f"  总还款额: ¥{equal['total_payment']:,.2f}\n")
            self.loan_result_text.insert(tk.END, f"  总利息: ¥{equal['total_interest']:,.2f}\n\n")

            # 等额本金
            equal_principal = comparison['equal_principal']
            self.loan_result_text.insert(tk.END, f"{equal_principal['method']}:\n")
            self.loan_result_text.insert(tk.END, f"  首月还款: ¥{equal_principal['first_month_payment']:,.2f}\n")
            self.loan_result_text.insert(tk.END, f"  末月还款: ¥{equal_principal['last_month_payment']:,.2f}\n")
            self.loan_result_text.insert(tk.END, f"  总还款额: ¥{equal_principal['total_payment']:,.2f}\n")
            self.loan_result_text.insert(tk.END, f"  总利息: ¥{equal_principal['total_interest']:,.2f}\n\n")

            # 利息差额和推荐
            self.loan_result_text.insert(tk.END, f"利息差额: ¥{comparison['interest_difference']:,.2f}\n")
            self.loan_result_text.insert(tk.END, f"推荐: {comparison['recommendation']}\n")

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