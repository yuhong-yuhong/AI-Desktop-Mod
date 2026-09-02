"""
AI模型基类
"""
from abc import ABC, abstractmethod
from typing import Iterator, List, Dict


class BaseAIModel(ABC):
    """AI模型基类 - 定义所有AI模型需要实现的接口"""
    
    def __init__(self, api_key: str):
        """
        初始化基础AI模型
        
        Args:
            api_key: API密钥
        """
        self.api_key = api_key
        self.conversation_history: List[Dict[str, str]] = []
    
    def add_to_history(self, role: str, content: str) -> None:
        """
        添加消息到对话历史
        
        Args:
            role: 消息角色 ('user' 或 'assistant')
            content: 消息内容
        """
        self.conversation_history.append({
            "role": role,
            "content": content
        })
    
    def get_context(self) -> List[Dict[str, str]]:
        """
        获取对话上下文
        
        Returns:
            对话历史列表
        """
        return self.conversation_history
    
    def clear_history(self) -> None:
        """清空对话历史"""
        self.conversation_history = []
    
    @abstractmethod
    def chat(self, message: str) -> str:
        """
        单条消息对话
        
        Args:
            message: 用户消息
            
        Returns:
            AI响应
        """
        pass
    
    @abstractmethod
    def chat_stream(self, message: str) -> Iterator[str]:
        """
        流式对话
        
        Args:
            message: 用户消息
            
        Yields:
            响应文本片段
        """
        pass
