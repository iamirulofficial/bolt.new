from __future__ import annotations

from .azure_openai_client import AzureOpenAIClient
from .gemini_client import GeminiClient
from .openai_client import OpenAIClient


def create_client(provider: str, **kwargs):
  provider = provider.lower()
  if provider == "openai":
    return OpenAIClient(**kwargs)
  if provider == "azure":
    return AzureOpenAIClient(**kwargs)
  if provider == "gemini":
    return GeminiClient(**kwargs)
  raise ValueError(f"Unknown provider: {provider}")
