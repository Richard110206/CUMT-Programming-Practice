import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QGridLayout, QPushButton, QLineEdit, QSizePolicy, QLabel)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("计算器")
        self.setGeometry(100, 100, 360, 500)
        
        # 计算器状态变量
        self.current_input = "0"  # 当前显示的数字
        self.expression = ""  # 完整表达式
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        self.set_styles()
        
        self.create_display()
        
        self.create_buttons()
    
    def set_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                padding: 10px;
                color: black;
            }
            QLabel {
                background-color: white;
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                padding: 5px;
                color: black;
                font-size: 14px;
                min-height: 20px;
            }
            QPushButton {
                background-color: #e0e0e0;
                border: none;
                border-radius: 4px;
                padding: 15px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
            QPushButton#operator {
                background-color: #f0ad4e;
                color: white;
            }
            QPushButton#operator:hover {
                background-color: #ec971f;
            }
            QPushButton#equal {
                background-color: #5cb85c;
                color: white;
            }
            QPushButton#equal:hover {
                background-color: #449d44;
            }
            QPushButton#clear {
                background-color: #d9534f;
                color: white;
            }
            QPushButton#clear:hover {
                background-color: #c9302c;
            }
        """)
    
    def create_display(self):
        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setText("0")
        self.display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.display.setMinimumHeight(60)
        self.display.setFont(QFont("Arial", 24))
        self.display.setStyleSheet("color: black;")
        
        self.main_layout.addWidget(self.display)
        
        # 使用 QLabel 来显示历史记录
        self.history_label = QLabel()
        self.history_label.setAlignment(Qt.AlignRight)
        self.history_label.setText("")
        self.history_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.history_label.setMinimumHeight(30)
        self.history_label.setFont(QFont("Arial", 12))
        
        self.main_layout.addWidget(self.history_label)
    
    def create_buttons(self):
        self.buttons_layout = QGridLayout()
        self.buttons_layout.setSpacing(5)
        
        # 按钮文本和位置
        buttons = [
            ("C", 0, 0, 1, 1, "clear"),
            ("±", 0, 1, 1, 1, "normal"),
            ("%", 0, 2, 1, 1, "normal"),
            ("÷", 0, 3, 1, 1, "operator"),
            
            ("7", 1, 0, 1, 1, "normal"),
            ("8", 1, 1, 1, 1, "normal"),
            ("9", 1, 2, 1, 1, "normal"),
            ("×", 1, 3, 1, 1, "operator"),
            
            ("4", 2, 0, 1, 1, "normal"),
            ("5", 2, 1, 1, 1, "normal"),
            ("6", 2, 2, 1, 1, "normal"),
            ("-", 2, 3, 1, 1, "operator"),
            
            ("1", 3, 0, 1, 1, "normal"),
            ("2", 3, 1, 1, 1, "normal"),
            ("3", 3, 2, 1, 1, "normal"),
            ("+", 3, 3, 1, 1, "operator"),
            
            ("0", 4, 0, 1, 2, "normal"),
            (".", 4, 2, 1, 1, "normal"),
            ("=", 4, 3, 1, 1, "equal")
        ]
        
        for button_text, row, col, rowspan, colspan, button_type in buttons:
            button = QPushButton(button_text)
            button.setObjectName(button_type)
            
            if button_type == "normal":
                if button_text.isdigit():  # 数字按钮
                    button.clicked.connect(lambda _, digit=button_text: self.number_clicked(digit))
                elif button_text == ".":  # 小数点按钮
                    button.clicked.connect(self.decimal_clicked)
                elif button_text == "±":  # 正负号按钮
                    button.clicked.connect(self.sign_clicked)
                elif button_text == "%":  # 百分号按钮
                    button.clicked.connect(self.percent_clicked)
            elif button_type == "operator":
                button.clicked.connect(lambda _, op=button_text: self.operator_clicked(op))
            elif button_type == "equal":
                button.clicked.connect(self.equal_clicked)
            elif button_type == "clear":
                button.clicked.connect(self.clear_clicked)
                
            self.buttons_layout.addWidget(button, row, col, rowspan, colspan)
        
        self.main_layout.addLayout(self.buttons_layout)
    
    def number_clicked(self, digit):
        """处理数字按钮点击"""
        if self.current_input == "0":
            self.current_input = digit
        else:
            self.current_input += digit
        
        self.display.setText(self.current_input)
    
    def decimal_clicked(self):
        """处理小数点按钮点击"""
        if "." not in self.current_input:
            if self.current_input == "0":
                self.current_input = "0."
            else:
                self.current_input += "."
            self.display.setText(self.current_input)
    
    def sign_clicked(self):
        """处理正负号按钮点击"""
        if self.current_input != "0":
            if self.current_input.startswith("-"):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            self.display.setText(self.current_input)
    
    def percent_clicked(self):
        """处理百分号按钮点击"""
        try:
            value = float(self.current_input)
            value /= 100
            self.current_input = str(value)
            if value.is_integer():
                self.current_input = str(int(value))
            self.display.setText(self.current_input)
        except:
            self.display.setText("错误")
            self.current_input = "0"
    
    def operator_clicked(self, operator):
        """处理操作符按钮点击"""
        # 将当前数字和操作符添加到表达式中
        if self.expression:
            self.expression += " " + self.current_input + " " + operator
        else:
            self.expression = self.current_input + " " + operator
        
        # 更新历史记录显示
        self.history_label.setText(self.expression)
        
        # 重置当前输入
        self.current_input = "0"
        
        self.display.setText("0")
    
    def equal_clicked(self):
        """处理等号按钮点击"""
        if self.expression:
            # 构建完整表达式
            full_expression = self.expression + " " + self.current_input
            
            # 显示完整表达式
            self.history_label.setText(full_expression + " =")
            
            # 计算表达式
            try:
                result = self.calculate_expression(full_expression)
                self.current_input = str(result)
                if result.is_integer():
                    self.current_input = str(int(result))
                self.display.setText(self.current_input)
                
                # 重置表达式
                self.expression = ""
            except Exception as e:
                self.display.setText("错误")
                self.expression = ""
        else:
            # 如果没有表达式，直接显示当前输入
            self.history_label.setText(self.current_input + " =")
    
    def clear_clicked(self):
        """处理清除按钮点击"""
        # 保存当前表达式作为历史记录
        if self.expression or self.current_input != "0":
            full_expression = self.expression + " " + self.current_input if self.expression else self.current_input
            self.history_label.setText(full_expression + " = " + self.display.text())
        
        # 重置计算器
        self.reset_calculator()
    
    def calculate_expression(self, expression):
        """使用栈计算表达式，支持先乘除后加减"""
        # 分割表达式为tokens
        tokens = expression.split()
        
        # 第一步：处理乘除运算
        values = []  # 存储数值
        operators = []  # 存储操作符
        
        i = 0
        while i < len(tokens):
            token = tokens[i]
            
            if self.is_number(token):
                values.append(float(token))
            elif token in ['×', '÷']:
                # 立即处理乘除运算
                if values and i + 1 < len(tokens) and self.is_number(tokens[i + 1]):
                    op = token
                    left = values.pop()
                    right = float(tokens[i + 1])
                    
                    if op == '×':
                        values.append(left * right)
                    elif op == '÷':
                        if right == 0:
                            raise ZeroDivisionError("除以零")
                        values.append(left / right)
                    
                    i += 1  # 跳过下一个数字
                else:
                    raise ValueError("表达式格式错误")
            else:
                # 加减运算符和数字直接入栈
                operators.append(token)
                if i + 1 < len(tokens) and self.is_number(tokens[i + 1]):
                    values.append(float(tokens[i + 1]))
                    i += 1
            
            i += 1
        
        # 第二步：处理加减运算
        result = values[0] if values else 0
        value_index = 1
        
        for op in operators:
            if op == '+':
                result += values[value_index]
            elif op == '-':
                result -= values[value_index]
            value_index += 1
        
        return result
    
    def is_number(self, s):
        """判断字符串是否为数字"""
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    def reset_calculator(self):
        """重置计算器状态"""
        self.current_input = "0"
        self.expression = ""
        self.display.setText("0")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())