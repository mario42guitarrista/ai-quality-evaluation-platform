from services.llm_service import generate_response_with_provider

from types import SimpleNamespace

import pytest

from providers.gemini_provider import GeminiProvider


class FakeInteractions:

    def __init__(self, output_text: str):
        self.output_text = output_text
        self.last_request = None

    def create(self, **kwargs):
        self.last_request = kwargs

        return SimpleNamespace(
            output_text=self.output_text
        )


class FakeGeminiClient:

    def __init__(self, output_text: str):
        self.interactions = FakeInteractions(output_text)


def test_gemini_provider_generates_response():
    fake_client = FakeGeminiClient(
        output_text="Gemini test response"
    )

    provider = GeminiProvider(
        model="gemini-3.5-flash-lite",
        client=fake_client
    )

    response = provider.generate_response(
        prompt="Explain regression testing."
    )

    assert response == "Gemini test response"
    assert fake_client.interactions.last_request == {
        "model": "gemini-3.5-flash-lite",
        "input": "Explain regression testing.",
        "store": False
    }


def test_gemini_provider_requires_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    with pytest.raises(ValueError, match="GEMINI_API_KEY"):
        GeminiProvider()


def test_gemini_provider_rejects_empty_response():
    fake_client = FakeGeminiClient(output_text="")

    provider = GeminiProvider(
        client=fake_client
    )

    with pytest.raises(RuntimeError, match="empty response"):
        provider.generate_response(
            prompt="Explain smoke testing."
        )

def test_llm_service_uses_gemini_provider():
    fake_client = FakeGeminiClient(
        output_text="Gemini service response"
    )

    response = generate_response_with_provider(
        prompt="Explain exploratory testing.",
        provider_name="gemini",
        model="gemini-3.5-flash-lite",
        provider_options={
            "client": fake_client
        }
    )

    assert response == "Gemini service response"