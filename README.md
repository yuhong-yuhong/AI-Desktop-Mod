# AI-Desktop-Mod
虚拟桌面应用AI对话Mod示例 - 集成LLM语言模型与对话栏交互

## 说明
这是一个最小可运行的 PyCharm 示例：
- 使用 tkinter 提供一个简单的聊天窗口（main.py）
- ai_client.py 提供一个轻量的 AI 后端适配器（支持 OpenAI，其他为占位）
- config.py 已包含应用配置

## 运行方法（在 PyCharm 中）
1. 克隆仓库并打开为项目。
2. 创建并激活 Python 虚拟环境（建议 Python 3.8+）。
3. 在 PyCharm 中将项目解释器指向该虚拟环境。
4. 安装依赖：
   - 使用 PyCharm 的依赖管理或运行: pip install -r requirements.txt
5. 可选：复制 `.env.example` 为 `.env` 并填写 `OPENAI_API_KEY` 来启用真实的 OpenAI 调用。
6. 运行 `main.py`（右键 -> Run）

## 开发提示
- 若希望接入本地模型，将你的适配器实现放到 `ai_models/` 并在 `config.AI_MODEL` 设为 `local`。
- 当前实现对缺失 API Key 回退为模拟回答，方便离线测试。
