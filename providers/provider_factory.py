from typing import Any

from providers.gemini_provider import GeminiProvider
from providers.mock_provider import MockProvider
from providers.openai_provider import OpenAIProvider


PROVIDERS = {
    "openai": OpenAIProvider,
    "gemini": GeminiProvider,
    "mock": MockProvider
}


def get_provider(
    provider_name: str,
    model: str,
    **provider_options: Any
):
    provider_class = PROVIDERS.get(provider_name)

    if provider_class is None:
        supported_providers = ", ".join(PROVIDERS.keys())

        raise ValueError(
            f"Provider '{provider_name}' is not supported. "
            f"Supported providers: {supported_providers}"
        )

    return provider_class(
        model=model,
        **provider_options
    )