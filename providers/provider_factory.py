from providers.mock_provider import MockProvider
from providers.openai_provider import OpenAIProvider


PROVIDERS = {
    "openai": OpenAIProvider,
    "mock": MockProvider
}


def get_provider(provider_name: str, model: str):
    provider_class = PROVIDERS.get(provider_name)

    if provider_class is None:
        supported_providers = ", ".join(PROVIDERS.keys())
        raise ValueError(
            f"Provider '{provider_name}' is not supported. "
            f"Supported providers: {supported_providers}"
        )

    return provider_class(model=model)
