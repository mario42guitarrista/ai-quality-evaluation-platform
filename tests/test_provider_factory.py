import pytest

from providers.gemini_provider import GeminiProvider
from providers.openai_provider import OpenAIProvider
from providers.provider_factory import get_provider


def test_get_openai_provider():
    provider = get_provider(
        provider_name="openai",
        model="gpt-4.1-mini"
    )

    assert isinstance(provider, OpenAIProvider)


def test_unsupported_provider_raises_error():
    with pytest.raises(ValueError) as error:
        get_provider(
            provider_name="unsupported-provider",
            model="test-model"
        )

    assert "unsupported-provider" in str(error.value)
    assert "Supported providers" in str(error.value)


def test_get_gemini_provider(monkeypatch):
    monkeypatch.setenv(
        "GEMINI_API_KEY",
        "test-gemini-api-key"
    )

    provider = get_provider(
        provider_name="gemini",
        model="gemini-3.5-flash-lite"
    )

    assert isinstance(provider, GeminiProvider)
    assert provider.model == "gemini-3.5-flash-lite"