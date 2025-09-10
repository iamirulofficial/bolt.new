from __future__ import annotations

import os

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


def client_from_env():
  provider = os.getenv("LLM_PROVIDER", "openai").lower()
  if provider == "openai":
    return create_client(
      provider,
      api_key=os.environ["OPENAI_API_KEY"],
      model=os.getenv("OPENAI_MODEL", "gpt-4o"),
    )
  if provider == "azure":
    return create_client(
      provider,
      api_key=os.environ["AZURE_OPENAI_API_KEY"],
      endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
      deployment=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    )
  if provider == "gemini":
    return create_client(
      provider,
      api_key=os.environ["GEMINI_API_KEY"],
      model=os.getenv("GEMINI_MODEL", "gemini-pro"),
    )
  raise ValueError(f"Unknown provider: {provider}")
