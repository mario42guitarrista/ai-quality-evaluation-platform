from types import SimpleNamespace

from providers.base_provider import ProviderGenerationResult
from providers.openai_provider import OpenAIProvider


class FakeChatCompletions:

    def __init__(self):
        self.last_request = None

    def create(self, **kwargs):
        self.last_request = kwargs

        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content="OpenAI test response"
                    )
                )
            ],
            usage=SimpleNamespace(
                prompt_tokens=100,
                completion_tokens=25,
                total_tokens=125,
                prompt_tokens_details=SimpleNamespace(
                    cached_tokens=20
                ),
                completion_tokens_details=SimpleNamespace(
                    reasoning_tokens=5
                )
            )
        )


class FakeOpenAIClient:

    def __init__(self):
        self.chat = SimpleNamespace(
            completions=FakeChatCompletions()
        )


def test_openai_provider_returns_usage_metadata():
    fake_client = FakeOpenAIClient()

    provider = OpenAIProvider(
        model="gpt-4.1-mini",
        client=fake_client
    )

    result = provider.generate_response_with_usage(
        "Explain regression testing."
    )

    assert result == ProviderGenerationResult(
        text="OpenAI test response",
        input_tokens=100,
        output_tokens=25,
        total_tokens=125,
        cached_input_tokens=20,
        reasoning_tokens=5
    )

    assert fake_client.chat.completions.last_request == {
        "model": "gpt-4.1-mini",
        "messages": [
            {
                "role": "user",
                "content": "Explain regression testing."
            }
        ]
    }


def test_openai_provider_preserves_text_response():
    provider = OpenAIProvider(
        client=FakeOpenAIClient()
    )

    response = provider.generate_response(
        "Explain smoke testing."
    )

    assert response == "OpenAI test response"