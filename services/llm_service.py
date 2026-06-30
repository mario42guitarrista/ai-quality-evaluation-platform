from providers.openai_provider import OpenAIProvider


def generate_response_with_provider(
    prompt: str,
    provider_name: str = "openai",
    model: str = "gpt-4.1-mini"
) -> str:

    if provider_name == "openai":
        provider = OpenAIProvider(model=model)
        return provider.generate_response(prompt)

    raise ValueError(f"Provider not supported: {provider_name}")