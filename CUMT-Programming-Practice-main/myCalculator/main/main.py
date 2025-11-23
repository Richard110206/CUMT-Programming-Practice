"""
myCalculator 主程序入口
启动多功能计算器应用程序
"""

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from ui.main_window import main

    if __name__ == "__main__":
        print("正在启动 myCalculator 多功能计算器...")
        print("项目根目录:", project_root)
        print("=" * 50)

        # 检查依赖
        try:
            import tkinter
            print("✓ tkinter 模块已加载")
        except ImportError:
            print("✗ tkinter 模块未找到")
            print("请安装 tkinter: sudo apt-get install python3-tk (Ubuntu/Debian)")
            sys.exit(1)

        try:
            import requests
            print("✓ requests 模块已加载")
        except ImportError:
            print("⚠ requests 模块未找到，货币转换功能将不可用")
            print("请安装 requests: pip install requests")

        print("=" * 50)
        print("启动图形界面...")

        # 启动应用程序
        main()

except Exception as e:
    print(f"程序启动失败: {str(e)}")
    print("=" * 50)
    print("可能的解决方案:")
    print("1. 确保安装了所有依赖: pip install -r requirements.txt")
    print("2. 检查Python版本是否兼容 (推荐Python 3.7+)")
    print("3. 确保系统支持tkinter图形界面")
    print("=" * 50)
    sys.exit(1)