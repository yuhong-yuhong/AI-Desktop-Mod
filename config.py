"""
配置文件 - 所有应用配置集中管理（已扩展 Deepseek 配置）
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ============ API 配置 ============
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-key")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "your-claude-key")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "your-deepseek-key")
LOCAL_MODEL_URL = os.getenv("LOCAL_MODEL_URL", "http://localhost:11434")

# ============ AI 模型选择 ============
# 可选: "openai", "claude", "local", "deepseek"
# 默认改为 "local"，方便在没有外部 API Key 时直接运行示例。
AI_MODEL = os.getenv("AI_MODEL", "local")

# 模型参数
MODEL_CONFIG = {
    "openai": {
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "max_tokens": 2000,
    },
    "claude": {
        "model": "claude-3-sonnet-20240229",
        "temperature": 0.7,
        "max_tokens": 2000,
    },
    "local": {
        "model": "llama2",
        "temperature": 0.7,
        "num_predict": 2000,
    },
    # Deepseek - OpenAI 兼容 API 的示例配置
    "deepseek": {
        # 请使用 Deepseek 提供的 API base URL，例如: "https://api.deepseek.example/v1"
        "api_base": os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.example/v1"),
        "model": os.getenv("DEEPSEEK_MODEL", "deepseek-1.0"),
        "temperature": float(os.getenv("DEEPSEEK_TEMPERATURE", "0.7")),
        "max_tokens": int(os.getenv("DEEPSEEK_MAX_TOKENS", "2000")),
    }
}

# ============ UI 配置 ============
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "AI Desktop Chat Mod"

# UI样式
THEME = "light"  # "light" 或 "dark"
FONT_SIZE = 10
FONT_FAMILY = "Arial"

# ============ 对话配置 ============
MAX_HISTORY = 100  # 保存的最大对话数
STREAM_OUTPUT = True  # 是否流式输出
AUTO_SAVE = True  # 自动保存对话
SAVE_INTERVAL = 300  # 自动保存间隔(秒)

# ============ 数据路径 ============
DATA_DIR = "./data"
HISTORY_FILE = os.path.join(DATA_DIR, "chat_history.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
LOG_FILE = os.path.join(DATA_DIR, "app.log")

# 确保数据目录存在
os.makedirs(DATA_DIR, exist_ok=True)

# ============ 日志配置 ============
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============ 系统提示词 ============
SYSTEM_PROMPT = """你是一个有帮助的AI助手。
- 回答用户的问题
- 提供有用的建议
- 保持友好和专业的语气
- 如果不确定，请说明"""
