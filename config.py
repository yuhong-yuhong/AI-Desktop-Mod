"""
配置文件 - Deepseek AI对话配置集中管理
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ============ Deepseek API 配置 ============
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "your-deepseek-key")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")

# ============ 模型参数 ============
MODEL_CONFIG = {
    "deepseek": {
        "model": "deepseek-chat",
        "temperature": 0.7,
        "max_tokens": 2000,
        "top_p": 0.95,
    }
}

# ============ UI 配置 ============
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
WINDOW_TITLE = "Deepseek AI Chat"

# UI样式
THEME = "light"  # "light" 或 "dark"
FONT_SIZE = 10
FONT_FAMILY = "Arial"

# ============ 对话配置 ============
MAX_HISTORY = 50  # 保存的最大对话对数（考虑token限制）
STREAM_OUTPUT = True  # 是否流式输出
AUTO_SAVE = True  # 自动保存对话
SAVE_INTERVAL = 300  # 自动保存间隔(秒)

# ============ 数据路径 ============
DATA_DIR = "./data"
HISTORY_FILE = os.path.join(DATA_DIR, "chat_history.json")
LOG_FILE = os.path.join(DATA_DIR, "app.log")

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)

# ============ 日志配置 ============
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============ 系统提示词 ============
SYSTEM_PROMPT = """你是一个有帮助的AI助手，由Deepseek提供支持。
- 回答用户的问题
- 提供有用的建议
- 保持友好和专业的语气
- 如果不确定，请说明"""