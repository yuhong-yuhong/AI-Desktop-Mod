"""
Minimal base class for AI models used by the application.
"""
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class BaseAIModel:
    """
    Minimal base class that provides history management and a simple interface
    for model implementations. Child classes should implement chat/chat_stream.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.history: List[Dict[str, str]] = []

    def add_to_history(self, role: str, content: str) -> None:
        """Add a message to the local history buffer."""
        self.history.append({"role": role, "content": content})
        # Keep the history bounded to avoid memory blowup
        if len(self.history) > 200:
            self.history = self.history[-200:]

    def get_context(self, max_messages: int = 10):
        """Return the last N messages formatted for ChatCompletion-like APIs."""
        msgs = self.history[-max_messages:]
        return [{"role": m["role"], "content": m["content"]} for m in msgs]

    def chat(self, message: str) -> str:
        raise NotImplementedError

    def chat_stream(self, message: str):
        raise NotImplementedError
