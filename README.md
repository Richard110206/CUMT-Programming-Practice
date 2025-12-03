# CUMT程序设计综合实践 🎯

<p>
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen.svg" alt="Status">
  <img src="https://img.shields.io/badge/Project-Educational%20Final-orange.svg" alt="Project Type">
</p>


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
<p>
  <img src="https://img.shields.io/badge/Framework-Tkinter-8dd2f7.svg" alt="Tkinter">
  <img src="https://img.shields.io/badge/Features-Multi--functional-ff69b4.svg" alt="Features">
  <img src="https://img.shields.io/badge/Status-Complete-success.svg" alt="Status">
</p>

一个功能丰富的计算器应用，支持：
- 基础四则运算
- 高级数学函数
- 进制转换
- 长度单位转换
- 货币汇率转换
- 贷款计算器

### 🎮 趣味拼图游戏 (Puzzle_Master)
<p>
  <img src="https://img.shields.io/badge/Framework-PyQt5-41cd52.svg" alt="PyQt5">
  <img src="https://img.shields.io/badge/Game-Mode-Multiple-9cf.svg" alt="Game Mode">
  <img src="https://img.shields.io/badge/Difficulty-2x2--to--6x6-fd7e14.svg" alt="Difficulty">
  <img src="https://img.shields.io/badge/Features-Leaderboard-e83e8c.svg" alt="Features">
</p>

支持多种游戏模式的拼图游戏：
- 休闲模式：自由选择难度
- 挑战模式：计时计步排行榜
- 多种难度等级（2×2 到 6×6）
- 自定义图片支持

### 📝 智能文本编辑器 (TextEditor)
<p>
  <img src="https://img.shields.io/badge/Framework-Tkinter-8dd2f7.svg" alt="Tkinter">
  <img src="https://img.shields.io/badge/AI-Integrated-007bff.svg" alt="AI Integration">
  <img src="https://img.shields.io/badge/Features-Syntax%20Highlighting-28a745.svg" alt="Features">
  <img src="https://img.shields.io/badge/Interface-Multi--tab-ffc107.svg" alt="Interface">
</p>

功能完整的文本编辑器：
- 语法高亮
- 智能AI助手集成（支持DeepSeek API）
- 多标签页支持
- 文件管理功能
- AI文本续写和总结功能

**技术栈**: Python, Tkinter, API集成

⚠️ **重要提示**: 要使用AI功能，需要配置API密钥！详见下方环境配置说明。

## 🛠️ 安装要求

### 系统要求
- Python 3.8+
- Windows/macOS/Linux

### 依赖安装
```bash
# 安装PyQt5（仅拼图游戏需要）
pip install PyQt5

# 安装文本编辑器依赖（包括dotenv）
pip install python-dotenv requests

# 安装其他依赖（如果需要）
pip install -r requirements.txt
```

### 🔑 API密钥配置（文本编辑器AI功能）

要使用文本编辑器的AI功能，需要配置DeepSeek API密钥：

1. **获取API密钥**
   - 访问 [DeepSeek官网](https://platform.deepseek.com) 注册账号
   - 在控制台中创建新的API密钥

2. **创建环境配置文件**
   ```bash
   cd TextEditor
   touch .env
   ```

3. **编辑.env文件**
   ```env
   DEEPSEEK_API_KEY=你的API密钥
   BASE_URL=https://api.deepseek.com/v1/chat/completions
   ```

4. **支持其他大模型API**
   你也可以配置其他兼容OpenAI格式的API：
   ```env
   # 例如使用其他API服务
   DEEPSEEK_API_KEY=你的API密钥
   BASE_URL=https://你的API服务地址/v1/chat/completions
   ```

⚠️ **注意事项**：
- 请妥善保管你的API密钥，不要将其提交到代码仓库
- 如果没有配置API密钥，文本编辑器仍可正常使用，但AI功能将返回模拟数据

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

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 感谢中国矿业大学提供的编程实践课程平台
- 感谢所有贡献者的努力和支持

---

⭐ 如果这个项目对你有帮助，请给个 Star！

---

<p align="center">
  <img src="https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg?style=flat-square" alt="Contributions Welcome">
  <img src="https://img.shields.io/badge/Forks-0-lightgrey.svg?style=flat-square" alt="Forks">
  <img src="https://img.shields.io/badge/Stars-0-yellow.svg?style=flat-square" alt="Stars">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Made%20with-Python-red.svg?style=flat-square" alt="Made with Python">
</p>

<p align="center">
  <a href="#top">回到顶部 🔝</a>
</p>
