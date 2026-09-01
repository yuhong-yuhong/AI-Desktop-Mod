"""
Deepseek API集成
"""
import openai
from typing import Iterator
from ai_models.base import BaseAIModel
from config import SYSTEM_PROMPT, MODEL_CONFIG, DEEPSEEK_API_KEY
import logging

logger = logging.getLogger(__name__)


class DeepseekModel(BaseAIModel):
    """Deepseek模型 - 使用OpenAI兼容API"""
    
    def __init__(self, api_key: str = DEEPSEEK_API_KEY):
        """
        初始化Deepseek模型
        
        Args:
            api_key: Deepseek API密钥
        """
        super().__init__(api_key)
        
        # 配置OpenAI客户端以使用Deepseek API
        openai.api_key = api_key
        openai.api_base = MODEL_CONFIG["deepseek"]["api_base"]
        
        self.model_name = MODEL_CONFIG["deepseek"]["model"]
        self.temperature = MODEL_CONFIG["deepseek"]["temperature"]
        self.max_tokens = MODEL_CONFIG["deepseek"]["max_tokens"]
        
        logger.info(f"Deepseek模型初始化完成: {self.model_name}")
    
    def chat(self, message: str) -> str:
        """
        单条消息对话
        
        Args:
            message: 用户消息
            
        Returns:
            AI响应
        """
        try:
            # 添加用户消息到历史
            self.add_to_history("user", message)
            
            # 构建请求
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *self.get_context()
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            
            # 提取响应
            assistant_message = response.choices[0].message.content
            self.add_to_history("assistant", assistant_message)
            
            logger.info("成功获取Deepseek响应")
            return assistant_message
            
        except Exception as e:
            logger.error(f"Deepseek API错误: {str(e)}")
            raise
    
    def chat_stream(self, message: str) -> Iterator[str]:
        """
        流式对话 - 实时返回响应片段
        
        Args:
            message: 用户消息
            
        Yields:
            响应文本片段
        """
        try:
            # 添加用户消息到历史
            self.add_to_history("user", message)
            
            # 构建流式请求
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *self.get_context()
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True,
            )
            
            # 收集完整响应
            full_response = ""
            
            for chunk in response:
                if "choices" in chunk and len(chunk["choices"]) > 0:
                    delta = chunk["choices"][0].get("delta", {})
                    if "content" in delta:
                        content = delta["content"]
                        full_response += content
                        yield content
            
            # 添加助手响应到历史
            if full_response:
                self.add_to_history("assistant", full_response)
                logger.info("流式响应完成")
                
        except Exception as e:
            logger.error(f"Deepseek流式API错误: {str(e)}")
            raise
