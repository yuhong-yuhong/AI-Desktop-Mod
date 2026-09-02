"""
OpenAI model implementation that uses the openai Python package.
"""
from typing import Iterator
import openai
import logging
from ai_models.base import BaseAIModel
from config import OPENAI_API_KEY, MODEL_CONFIG, SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class OpenAIModel(BaseAIModel):
    def __init__(self, api_key: str = None):
        super().__init__(api_key or OPENAI_API_KEY)
        openai.api_key = self.api_key
        cfg = MODEL_CONFIG.get("openai", {})
        self.model_name = cfg.get("model", "gpt-3.5-turbo")
        self.temperature = cfg.get("temperature", 0.7)
        self.max_tokens = cfg.get("max_tokens", 2000)
        logger.info(f"OpenAIModel initialized: {self.model_name}")

    def chat(self, message: str) -> str:
        self.add_to_history("user", message)
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, *self.get_context()],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            assistant_message = response.choices[0].message.content
            self.add_to_history("assistant", assistant_message)
            return assistant_message
        except Exception as e:
            logger.exception("OpenAI chat error")
            raise

    def chat_stream(self, message: str) -> Iterator[str]:
        self.add_to_history("user", message)
        try:
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, *self.get_context()],
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True,
            )
            full = ""
            for chunk in response:
                if hasattr(chunk, 'choices'):
                    # some backends may return objects
                    choices = chunk.choices
                else:
                    choices = chunk.get("choices", [])
                if len(choices) > 0:
                    delta = choices[0].get("delta", {}) if isinstance(choices[0], dict) else getattr(choices[0], 'delta', {})
                    content = None
                    if isinstance(delta, dict):
                        content = delta.get("content")
                    else:
                        content = getattr(delta, 'get', lambda k, d=None: None)("content")
                    if content:
                        full += content
                        yield content
            if full:
                self.add_to_history("assistant", full)
        except Exception as e:
            logger.exception("OpenAI stream error")
            raise
