# 简单 AI 客户端封装，支持 openai / claude / local 回退到模拟回答
import config


def _mock_reply(prompt: str) -> str:
    # 非常简单的回显/模拟逻辑，便于本地运行时测试
    return f"这是模拟回答：我收到了你的消息：{prompt}"


def get_response(user_text: str, history: list) -> str:
    """根据 config.AI_MODEL 选择后端并返回字符串回答。
    参数:
      - user_text: 本次用户文本
      - history: 消息历史，OpenAI 风格的 messages 列表
    返回: AI 文本回答
    """
    model = config.AI_MODEL.lower()

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

    if model == 'local':
        # 本地模型占位调用 - 若实现了本地 model，可在 ai_models 包中添加实现并导入
        try:
            from ai_models import local_model
            return local_model.generate(user_text)
        except Exception:
            return _mock_reply(user_text)

    # default: mock
    return _mock_reply(user_text)
