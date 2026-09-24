import os

from app.llm.base import BaseLLM
from app.llm.openrouter_llm import OpenRouterLLM


class LLMFactory:
    """
    Creates the configured LLM.

    Future providers:
    - OpenRouter
    - Ollama
    - Gemini
    - OpenAI
    """

    @staticmethod
    def create() -> BaseLLM:

        provider = os.getenv(
            "LLM_PROVIDER",
            "openrouter"
        ).lower()

        if provider == "openrouter":
            return OpenRouterLLM()

        raise ValueError(
            f"Unsupported LLM provider: {provider}"
        )