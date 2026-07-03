import pytest

from providers.provider_factory import get_provider
from providers.openai_provider import OpenAIProvider


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