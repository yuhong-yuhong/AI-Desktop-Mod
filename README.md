# Deepseek AI Desktop Chat

虚拟桌面应用 AI 对话 Mod - 集成 Deepseek 语言模型

## 功能说明

这是一个简洁高效的 Deepseek AI 聊天应用：
- 使用 tkinter 提供简单易用的聊天窗口
- 集成 Deepseek API 实现高质量 AI 对话
- 自动保存对话历史
- 支持流式输出和实时交互

## 项目结构

```
AI-Desktop-Mod/
├── main.py              # 主程序入口 - Tkinter UI
├── ai_client.py         # Deepseek API 客户端
├── config.py            # 配置文件
├── .env.example         # 环境变量示例
├── requirements.txt     # 依赖列表
└── README.md           # 项目文档
```

## 安装与运行

### 1. 环境准备
```bash
# 克隆仓库
git clone https://github.com/yuhong-yuhong/AI-Desktop-Mod.git
cd AI-Desktop-Mod

# 创建虚拟环境（推荐 Python 3.8+）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置 API Key
```bash
# 复制示例配置文件
cp .env.example .env

# 编辑 .env 文件，填入你的 Deepseek API Key
# DEEPSEEK_API_KEY=sk-xxxxx
# DEEPSEEK_API_URL=https://api.deepseek.com/v1/chat/completions
```

获取 Deepseek API Key：
- 访问 [Deepseek 官网](https://www.deepseek.com/)
- 注册账户并获取 API Key

### 4. 运行应用
```bash
python main.py
```

## 配置说明

编辑 `config.py` 调整应用参数：

```python
# 窗口大小
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700

# 对话参数
MAX_HISTORY = 50          # 最大历史记录数
STREAM_OUTPUT = True      # 启用流式输出
AUTO_SAVE = True          # 自动保存对话

# 模型参数
MODEL_CONFIG = {
    "deepseek": {
        "model": "deepseek-chat",
        "temperature": 0.7,       # 0-1，值越小输出越确定
        "max_tokens": 2000,       # 最大生成token数
        "top_p": 0.95            # 核采样参数
    }
}
```

## 使用示例

1. 启动应用后，在输入框输入问题
2. 按 Enter 或点击"发送"按钮
3. AI 将返回响应（支持中英文）
4. 对话历史自动保存到 `data/chat_history.json`

## 代码优化特点

✅ **仅保留 Deepseek 支持** - 移除 OpenAI/Claude/Local 冗余代码
✅ **简化配置管理** - 集中配置，易于维护
✅ **改进错误处理** - 完整的日志和异常捕获
✅ **优化依赖** - 移除不必要的第三方库
✅ **增强代码注释** - 清晰的文档和类型提示

## 故障排除

### 问题：API Key 错误
**解决**：检查 `.env` 文件中的 `DEEPSEEK_API_KEY` 是否正确填写

### 问题：连接超时
**解决**：检查网络连接，确保能访问 `api.deepseek.com`

### 问题：模拟回答
**解决**：API Key 未配置或格式错误，应用退回到模拟模式

## 开发建议

- 修改系统提示词可以改变 AI 的回答风格（`config.py` 中的 `SYSTEM_PROMPT`）
- 调整 `temperature` 参数可以控制回答的创意度
- 减少 `MAX_HISTORY` 可以降低 API 成本

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎提交 Issue 或 Pull Request。