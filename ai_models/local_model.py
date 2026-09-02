"""
Local mock model for offline testing. Returns canned / echo responses so the
example can run without API keys.
"""
from typing import Iterator
import time
import logging
from ai_models.base import BaseAIModel

logger = logging.getLogger(__name__)


class LocalModel(BaseAIModel):
    def __init__(self):
        super().__init__(api_key=None)
        self.model_name = "local-mock"
        logger.info("LocalModel (mock) initialized")

    def chat(self, message: str) -> str:
        self.add_to_history("user", message)
        # simple deterministic mock reply
        reply = f"[LocalModel] 收到: {message[:200]}"
        self.add_to_history("assistant", reply)
        return reply

    def chat_stream(self, message: str) -> Iterator[str]:
        self.add_to_history("user", message)
        text = f"[LocalModel-stream] 逐步回复: {message}"
        # yield in small chunks to simulate streaming
        for i in range(0, len(text), 20):
            chunk = text[i : i + 20]
            time.sleep(0.05)
            yield chunk
        self.add_to_history("assistant", text)
