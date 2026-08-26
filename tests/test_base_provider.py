from providers.base_provider import (
    BaseLLMProvider,
    ProviderGenerationResult,
)


class LegacyStubProvider(BaseLLMProvider):

    def generate_response(self, prompt: str) -> str:
        return f"legacy response: {prompt}"


def test_usage_wrapper_preserves_legacy_provider_behavior():
    provider = LegacyStubProvider()

    result = provider.generate_response_with_usage(
        "Explain smoke testing."
    )

    assert result == ProviderGenerationResult(
        text="legacy response: Explain smoke testing."
    )

    assert result.to_dict() == {
        "text": "legacy response: Explain smoke testing.",
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0,
        "cached_input_tokens": 0,
        "reasoning_tokens": 0
    }