from devcrew_ai.config import LLM_PROVIDER
from devcrew_ai.llm.base import BaseLLM
from devcrew_ai.llm.mock_llm import MockLLM
from devcrew_ai.llm.ollama_llm import OllamaLLM

def get_llm() -> BaseLLM:
    """Factory function to retrieve the configured LLM provider."""
    provider = LLM_PROVIDER.lower()
    if provider == "ollama":
        return OllamaLLM()
    else:
        return MockLLM()
