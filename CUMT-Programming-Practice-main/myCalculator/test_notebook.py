"""
测试ttk.Notebook功能
"""

import tkinter as tk
from tkinter import ttk

def test_notebook():
    root = tk.Tk()
    root.title("Notebook测试")
    root.geometry("400x300")

    # 创建Notebook
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # 创建几个测试标签页
    tab1 = ttk.Frame(notebook)
    tab2 = ttk.Frame(notebook)
    tab3 = ttk.Frame(notebook)

    notebook.add(tab1, text="标签页1")
    notebook.add(tab2, text="标签页2")
    notebook.add(tab3, text="标签页3")

    # 在每个标签页添加内容
    ttk.Label(tab1, text="这是第一个标签页", font=("Arial", 14)).pack(pady=20)
    ttk.Button(tab1, text="测试按钮1", command=lambda: print("标签页1按钮被点击")).pack(pady=10)

    ttk.Label(tab2, text="这是第二个标签页", font=("Arial", 14)).pack(pady=20)
    ttk.Button(tab2, text="测试按钮2", command=lambda: print("标签页2按钮被点击")).pack(pady=10)

    ttk.Label(tab3, text="这是第三个标签页", font=("Arial", 14)).pack(pady=20)
    ttk.Button(tab3, text="测试按钮3", command=lambda: print("标签页3按钮被点击")).pack(pady=10)

    # 添加点击事件监听
    def on_tab_changed(event):
        selected_tab = event.widget.index(event.widget.select())
        print(f"切换到标签页 {selected_tab + 1}")

    notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

    root.mainloop()

if __name__ == "__main__":
    test_notebook()