"""
Deepseek AI客户端 - 简化版本，仅保留Deepseek支持
"""
import json
import urllib.request
import urllib.error
import logging
import config

logger = logging.getLogger(__name__)


def _mock_reply(prompt: str) -> str:
    """模拟回答 - 用于API不可用时的回退"""
    return f"模拟回答：我收到了你的消息：{prompt}"


def _call_http_json(url: str, payload: dict, headers: dict = None, timeout: int = 30) -> tuple:
    """发送HTTP JSON请求"""
    data = json.dumps(payload).encode("utf-8")
    hdrs = {"Content-Type": "application/json"}
    if headers:
        hdrs.update(headers)
    
    try:
        req = urllib.request.Request(url, data=data, headers=hdrs, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.getcode(), resp.read().decode("utf-8")
    except Exception as e:
        logger.error(f"HTTP请求失败: {e}")
        raise


def _parse_deepseek_response(raw: str) -> str:
    """解析Deepseek API响应"""
    try:
        response = json.loads(raw)
        
        # 标准OpenAI格式
        if "choices" in response and len(response["choices"]) > 0:
            choice = response["choices"][0]
            if "message" in choice and "content" in choice["message"]:
                return choice["message"]["content"].strip()
        
        logger.warning(f"无法解析响应格式: {raw}")
        return _mock_reply("")
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析失败: {e}")
        return raw.strip()


def get_response(user_text: str, history: list) -> str:
    """
    调用Deepseek API获取响应
    
    Args:
        user_text: 用户输入文本
        history: 消息历史（OpenAI格式）
    
    Returns:
        AI的响应文本
    """
    try:
        api_key = config.DEEPSEEK_API_KEY
        api_url = config.DEEPSEEK_API_URL
        
        # 验证配置
        if not api_key or api_key.startswith('your-'):
            logger.warning("Deepseek API Key未配置")
            return _mock_reply(user_text)
        
        if not api_url:
            logger.warning("Deepseek API URL未配置")
            return _mock_reply(user_text)
        
        # 准备消息历史 - 限制数量以控制token消耗
        messages = history[-(config.MAX_HISTORY or 50):]
        msgs = []
        for m in messages:
            role = m.get('role')
            content = m.get('content')
            if role and content is not None:
                msgs.append({"role": role, "content": content})
        
        # 构建请求体
        payload = {
            "model": config.MODEL_CONFIG["deepseek"]["model"],
            "messages": msgs,
            "temperature": config.MODEL_CONFIG["deepseek"]["temperature"],
            "max_tokens": config.MODEL_CONFIG["deepseek"]["max_tokens"],
            "top_p": config.MODEL_CONFIG["deepseek"].get("top_p", 0.95),
            "stream": False
        }
        
        # 请求头
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        # 发送请求
        code, response_raw = _call_http_json(api_url, payload, headers=headers, timeout=60)
        
        # 处理响应
        if 200 <= code < 300:
            response_text = _parse_deepseek_response(response_raw)
            logger.info("成功获取Deepseek响应")
            return response_text if response_text else _mock_reply(user_text)
        else:
            logger.error(f"Deepseek API错误 - 状态码: {code}, 响应: {response_raw}")
            return _mock_reply(user_text)
    
    except Exception as e:
        logger.error(f"调用Deepseek API异常: {e}")
        return _mock_reply(user_text)