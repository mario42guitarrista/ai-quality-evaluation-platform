from typing import Any

from providers.provider_factory import get_provider


def generate_response_with_provider(
    prompt: str,
    provider_name: str = "openai",
    model: str = "gpt-4.1-mini",
    provider_options: dict[str, Any] | None = None
) -> str:
    provider = get_provider(
        provider_name=provider_name,
        model=model,
        **(provider_options or {})
    )

    return provider.generate_response(prompt)