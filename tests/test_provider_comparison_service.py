import pytest

from providers.base_provider import (
    BaseLLMProvider,
    ProviderGenerationResult,
)
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


class UsageAwareProvider(BaseLLMProvider):

    def __init__(self, model: str):
        self.model = model

    def generate_response(self, prompt: str) -> str:
        return f"usage-aware response: {prompt}"

    def generate_response_with_usage(
        self,
        prompt: str
    ) -> ProviderGenerationResult:
        return ProviderGenerationResult(
            text=f"usage-aware response: {prompt}",
            input_tokens=120,
            output_tokens=30,
            total_tokens=150,
            cached_input_tokens=20,
            reasoning_tokens=5
        )


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
    assert results[0].input_tokens == 0
    assert results[0].output_tokens == 0
    assert results[0].total_tokens == 0

    assert results[1].success is False
    assert results[1].response is None
    assert results[1].latency_ms == 250.0
    assert results[1].input_tokens == 0
    assert results[1].output_tokens == 0
    assert results[1].total_tokens == 0
    assert "Provider unavailable" in results[1].error


def test_comparison_collects_provider_usage_and_cost(
    monkeypatch
):
    monkeypatch.setitem(
        PROVIDERS,
        "openai",
        UsageAwareProvider
    )

    timestamps = iter([
        30.0,
        30.050
    ])

    service = MultiProviderComparisonService(
        clock=lambda: next(timestamps)
    )

    result = service.compare(
        prompt="Explain API testing.",
        providers=[
            ProviderConfiguration(
                provider_name="openai",
                model="gpt-4.1-mini"
            )
        ]
    )[0]

    assert result.success is True
    assert result.response == (
        "usage-aware response: Explain API testing."
    )
    assert result.latency_ms == 50.0
    assert result.input_tokens == 120
    assert result.output_tokens == 30
    assert result.total_tokens == 150
    assert result.cached_input_tokens == 20
    assert result.reasoning_tokens == 5

    assert (
        result.estimated_uncached_input_cost_usd
        == 0.00004
    )
    assert (
        result.estimated_cached_input_cost_usd
        == 0.000002
    )
    assert result.estimated_output_cost_usd == 0.000048
    assert result.estimated_total_cost_usd == 0.00009
    assert result.pricing_tier == "standard_paid"
    assert result.pricing_effective_date == "2026-08-20"
    assert result.cost_error is None
    assert result.error is None

    assert (
        result.to_dict()["estimated_total_cost_usd"]
        == 0.00009
    )


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