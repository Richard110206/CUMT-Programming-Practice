# CUMT编程实践项目集合 🎯

> 中国矿业大学编程实践课程项目集合，包含多个实用工具和趣味应用

## 📁 项目结构

```
CUMT-Programming-Practice/
├── myCalculator/          # 多功能计算器
├── Puzzle_Master/         # 趣味拼图游戏
├── TextEditor/           # 智能文本编辑器
├── README.md            # 项目说明文档
└── .gitignore           # Git忽略文件配置
```

## 🚀 项目列表

### 🧮 多功能计算器 (myCalculator)
一个功能丰富的计算器应用，支持：
- 基础四则运算
- 高级数学函数
- 进制转换
- 长度单位转换
- 货币汇率转换
- 贷款计算器

**技术栈**: Python, Tkinter

### 🎮 趣味拼图游戏 (Puzzle_Master)
支持多种游戏模式的拼图游戏：
- 休闲模式：自由选择难度
- 挑战模式：计时计步排行榜
- 多种难度等级（2×2 到 6×6）
- 自定义图片支持

**技术栈**: Python, PyQt5

### 📝 智能文本编辑器 (TextEditor)
功能完整的文本编辑器：
- 语法高亮
- 智能AI助手集成
- 多标签页支持
- 文件管理功能

**技术栈**: Python, Tkinter, API集成

## 🛠️ 安装要求

### 系统要求
- Python 3.8+
- Windows/macOS/Linux

### 依赖安装
```bash
# 安装PyQt5（仅拼图游戏需要）
pip install PyQt5

# 安装其他依赖（如果需要）
pip install -r requirements.txt
```

## 🎮 快速开始

### 运行计算器
```bash
cd myCalculator/ui
python calculator_window.py
```

### 运行拼图游戏
```bash
cd Puzzle_Master
python main.py
```

### 运行文本编辑器
```bash
cd TextEditor
python main_window.py
```

## 📸 项目截图

> [项目截图将在后续添加]

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 📝 更新日志

### v2.0.0 (2025-12-03)
- ✨ 优化拼图游戏完成体验和难度选择界面
- 🔧 清理冗余的 `__init__.py` 文件，优化项目结构
- 🧹 添加全面的 `.gitignore` 配置
- 🐛 修复导入路径问题

### v1.x.x
- 🎱 基础计算器添加括号功能和键盘输入支持
- 🎨 优化计算器界面样式
- 📝 智能文本编辑器集成AI助手

## 👥 作者

- **Richard110206** - *项目维护者*
- **Puzzle Master Team** - *拼图游戏开发团队*

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 感谢中国矿业大学提供的编程实践课程平台
- 感谢所有贡献者的努力和支持

---

⭐ 如果这个项目对你有帮助，请给个 Star！