"""ai_models/local_model.py

本地模型客户端占位实现。

- 尝试通过 config.LOCAL_MODEL_URL（例如 http://localhost:11434）向本地模型服务器发送 POST 请求，json 字段包含 prompt 和 max_tokens。
- 尽量兼容多种返回格式（直接文本、json 包含 text/result/generated_text/output、或 OpenAI-like choices 列表）。
- 如果请求或解析失败，回退到简单的模拟回答，避免整个程序崩溃。

你可以根据实际本地模型服务的 API 调整请求 URL 或 payload 结构。
"""

import json
import urllib.request
import urllib.error
import config

DEFAULT_TIMEOUT = 30


def generate(prompt: str, max_tokens: int | None = None, timeout: int = DEFAULT_TIMEOUT) -> str:
    """调用本地模型服务生成文本。

    参数:
      - prompt: 输入提示词
      - max_tokens: 令牌/长度上限，None 表示使用 config 中的默认值
      - timeout: 请求超时时间（秒）

    返回: 生成的文本（字符串）。
    如果调用失败，返回一个模拟回答字符串以保证调用方不会崩溃。
    """
    url = config.LOCAL_MODEL_URL
    if not url:
        return f"（本地模型未配置）这是模拟回答：我收到了你的消息：{prompt}"

    payload = {
        "prompt": prompt,
        "max_tokens": max_tokens or config.MODEL_CONFIG.get("local", {}).get("num_predict", 2000),
    }
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json"}

    try:
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            # 尝试解析为 JSON
            try:
                j = json.loads(raw)
            except Exception:
                # 非 JSON，直接返回原始文本
                return raw.strip()

            # 常见字段提取
            for key in ("text", "result", "response", "generated_text", "output"):
                if key in j:
                    return j[key]

            # OpenAI-like 格式
            choices = j.get("choices")
            if isinstance(choices, list) and len(choices) > 0:
                first = choices[0]
                if isinstance(first, dict):
                    for k in ("text", "message", "content"):
                        if k in first:
                            return first[k]

            # 兜底，返回整个 JSON 的文本表示
            return json.dumps(j, ensure_ascii=False)

    except urllib.error.HTTPError as e:
        # 返回错误的响应体（如果有），否则返回错误说明
        try:
            err = e.read().decode('utf-8')
            return f"（本地模型 HTTP 错误 {e.code}）{err}"
        except Exception:
            return f"（本地模型 HTTP 错误 {e.code}）"
    except Exception:
        # 回退到模拟回答，保证程序继续运行
        return f"（本地模型调用失败，使用回退模拟）这是模拟回答：我收到了你的消息：{prompt}"


def is_available(timeout: int = 3) -> bool:
    """快速探测本地模型 URL 是否能连通（GET 请求），主要用于健康检查。"""
    url = config.LOCAL_MODEL_URL
    if not url:
        return False
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False
