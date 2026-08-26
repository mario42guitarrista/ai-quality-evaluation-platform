from types import SimpleNamespace

from providers.base_provider import ProviderGenerationResult
from providers.gemini_provider import GeminiProvider


class FakeInteractions:

    def __init__(self):
        self.last_request = None

    def create(self, **kwargs):
        self.last_request = kwargs

        return SimpleNamespace(
            output_text="Gemini test response",
            usage=SimpleNamespace(
                total_input_tokens=80,
                total_output_tokens=20,
                total_thought_tokens=10,
                total_cached_tokens=5,
                total_tokens=110
            )
        )


class FakeGeminiClient:

    def __init__(self):
        self.interactions = FakeInteractions()


def test_gemini_provider_returns_usage_metadata():
    fake_client = FakeGeminiClient()

    provider = GeminiProvider(
        model="gemini-3.5-flash-lite",
        client=fake_client
    )

    result = provider.generate_response_with_usage(
        "Explain regression testing."
    )

    assert result == ProviderGenerationResult(
        text="Gemini test response",
        input_tokens=80,
        output_tokens=30,
        total_tokens=110,
        cached_input_tokens=5,
        reasoning_tokens=10
    )

    assert fake_client.interactions.last_request == {
        "model": "gemini-3.5-flash-lite",
        "input": "Explain regression testing.",
        "store": False
    }