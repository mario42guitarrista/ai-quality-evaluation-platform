import pytest

from providers.base_provider import BaseLLMProvider
from providers.provider_factory import PROVIDERS
from services.provider_comparison_service import (
    MultiProviderComparisonService,
    ProviderConfiguration,
)


class SuccessfulProvider(BaseLLMProvider):

    def __init__(
        self,
        model: str,
        response_prefix: str = "Response"
    ):
        self.model = model
        self.response_prefix = response_prefix

    def generate_response(self, prompt: str) -> str:
        return f"{self.response_prefix}: {prompt}"


class FailingProvider(BaseLLMProvider):

    def __init__(self, model: str):
        self.model = model

    def generate_response(self, prompt: str) -> str:
        raise RuntimeError("Provider unavailable")


def test_comparison_collects_results_and_isolates_failures(
    monkeypatch
):
    monkeypatch.setitem(
        PROVIDERS,
        "successful-provider",
        SuccessfulProvider
    )
    monkeypatch.setitem(
        PROVIDERS,
        "failing-provider",
        FailingProvider
    )

    timestamps = iter([
        10.0,
        10.125,
        20.0,
        20.250
    ])

    service = MultiProviderComparisonService(
        clock=lambda: next(timestamps)
    )

    results = service.compare(
        prompt="Explain regression testing.",
        providers=[
            ProviderConfiguration(
                provider_name="successful-provider",
                model="successful-model",
                provider_options={
                    "response_prefix": "Provider A"
                }
            ),
            ProviderConfiguration(
                provider_name="failing-provider",
                model="failing-model"
            )
        ]
    )

    assert len(results) == 2

    assert results[0].success is True
    assert results[0].response == (
        "Provider A: Explain regression testing."
    )
    assert results[0].latency_ms == 125.0
    assert results[0].error is None

    assert results[1].success is False
    assert results[1].response is None
    assert results[1].latency_ms == 250.0
    assert "Provider unavailable" in results[1].error


def test_comparison_rejects_empty_prompt():
    service = MultiProviderComparisonService()

    with pytest.raises(
        ValueError,
        match="Prompt cannot be empty"
    ):
        service.compare(
            prompt=" ",
            providers=[
                ProviderConfiguration(
                    provider_name="mock",
                    model="mock-model"
                )
            ]
        )


def test_comparison_requires_at_least_one_provider():
    service = MultiProviderComparisonService()

    with pytest.raises(
        ValueError,
        match="At least one provider"
    ):
        service.compare(
            prompt="Explain smoke testing.",
            providers=[]
        )