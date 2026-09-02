# 简单 AI 客户端封装，支持 openai / claude /deepseek / local 回退到模拟回答
import json
import urllib.request
import urllib.error
import config


def _mock_reply(prompt: str) -> str:
    # 非常简单的回显/模拟逻辑，便于本地运行时测试
    return f"这是模拟回答：我收到了你的消息：{prompt}"


def _call_http_json(url: str, payload: dict, headers: dict | None = None, timeout: int = 30) -> tuple[int, str]:
    data = json.dumps(payload).encode("utf-8")
    hdrs = {"Content-Type": "application/json"}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=data, headers=hdrs, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.getcode(), resp.read().decode("utf-8")


def _parse_response_text(raw: str):
    # 尝试解析为 JSON 并抽取常见字段；否则返回原始文本
    try:
        j = json.loads(raw)
    except Exception:
        return raw.strip()

    for key in ("text", "result", "response", "generated_text", "output"):
        if key in j:
            return j[key]

    choices = j.get("choices")
    if isinstance(choices, list) and len(choices) > 0:
        first = choices[0]
        if isinstance(first, dict):
            for k in ("text", "message", "content"):
                if k in first:
                    val = first[k]
                    # 如果是 dict，尝试提取 content 字段
                    if isinstance(val, dict):
                        return val.get("content", json.dumps(val, ensure_ascii=False))
                    return val

    return json.dumps(j, ensure_ascii=False)


def get_response(user_text: str, history: list) -> str:
    """根据 config.AI_MODEL 选择后端并返回字符串回答。
    参数:
      - user_text: 本次用户文本
      - history: 消息历史，OpenAI 风格的 messages 列表
    返回: AI 文本回答
    """
    model = (config.AI_MODEL or "").lower()

    if model == 'openai':
        try:
            import openai
            key = config.OPENAI_API_KEY
            if not key or key.startswith('your-'):
                return _mock_reply(user_text)
            openai.api_key = key
            params = config.MODEL_CONFIG.get('openai', {})
            messages = history[-(config.MAX_HISTORY or 10):]
            # ensure messages in OpenAI format
            msgs = []
            for m in messages:
                role = m.get('role')
                content = m.get('content')
                if role and content is not None:
                    msgs.append({"role": role, "content": content})
            resp = openai.ChatCompletion.create(
                model=params.get('model', 'gpt-3.5-turbo'),
                messages=msgs,
                temperature=params.get('temperature', 0.7),
                max_tokens=params.get('max_tokens', 500),
            )
            # get assistant content
            return resp['choices'][0]['message']['content'].strip()
        except Exception:
            return _mock_reply(user_text)

    if model == 'claude':
        # Claude 客户端未集成，这里回退到模拟
        return _mock_reply(user_text)

    if model == 'deepseek':
        # Deepseek: 通过 OpenAI 兼容的 HTTP API 调用 Deepseek 服务
        # 需在 .env 中配置 DEEPSEEK_URL 和 DEEPSEEK_API_KEY
        try:
            url = getattr(config, 'DEEPSEEK_URL', '')
            api_key = getattr(config, 'DEEPSEEK_API_KEY', '')
            
            if not url or not api_key or api_key.startswith('your-'):
                return _mock_reply(user_text)
            
            # 准备消息 - 确保格式为 OpenAI 兼容格式
            messages = history[-(config.MAX_HISTORY or 10):]
            msgs = []
            for m in messages:
                role = m.get('role')
                content = m.get('content')
                if role and content is not None:
                    msgs.append({"role": role, "content": content})
            
            # Deepseek API 请求体（兼容 OpenAI 格式）
            payload = {
                "model": "deepseek-chat",  # Deepseek 的模型名称
                "messages": msgs,
                "temperature": config.MODEL_CONFIG.get('deepseek', {}).get('temperature', 0.7),
                "max_tokens": config.MODEL_CONFIG.get('deepseek', {}).get('num_predict', 2000),
                "stream": False
            }
            
            headers = {
                "Authorization": f"Bearer {api_key}"
            }

            code, raw = _call_http_json(url, payload, headers=headers)
            if code >= 200 and code < 300:
                response_text = _parse_response_text(raw)
                return response_text.strip() if response_text else _mock_reply(user_text)
            else:
                print(f"Deepseek API 返回错误码: {code}, 响应: {raw}")
                return _mock_reply(user_text)
        except Exception as e:
            print(f"Deepseek 调用错误: {e}")
            return _mock_reply(user_text)

    if model == 'local':
        # 本地模型占位调用 - 若实现了本地 model，可在 ai_models 包中添加实现并导入
        try:
            from ai_models import local_model
            return local_model.generate(user_text)
        except Exception:
            return _mock_reply(user_text)

    # default: mock
    return _mock_reply(user_text)
