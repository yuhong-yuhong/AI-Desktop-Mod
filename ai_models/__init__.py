from config import AI_MODEL, OPENAI_API_KEY, CLAUDE_API_KEY, DEEPSEEK_API_KEY


def get_model():
    """Return a model instance according to AI_MODEL in config.

    Current supported name: 'deepseek', 'openai' (placeholder), 'local' (placeholder).
    """
    name = AI_MODEL.lower()
    if name == "deepseek":
        from .deepseek_model import DeepseekModel

        return DeepseekModel(api_key=DEEPSEEK_API_KEY)

    if name == "openai":
        # If you implement openai_model.py add it to ai_models and this will return it
        try:
            from .openai_model import OpenAIModel

            return OpenAIModel(api_key=OPENAI_API_KEY)
        except Exception as e:
            raise RuntimeError("OpenAIModel not implemented in ai_models") from e

    if name == "local":
        try:
            from .local_model import LocalModel

            return LocalModel()
        except Exception as e:
            raise RuntimeError("LocalModel not implemented in ai_models") from e

    raise RuntimeError(f"Unknown AI_MODEL: {AI_MODEL}")


__all__ = ["get_model"]
