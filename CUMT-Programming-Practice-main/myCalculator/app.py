
"""
myCalculator 主程序入口
启动多功能计算器应用程序
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from ui.calculator_window import main

    if __name__ == "__main__":
        main()

except Exception as e:
    print(f"程序启动失败: {str(e)}")
    sys.exit(1)