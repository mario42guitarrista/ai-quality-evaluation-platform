from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass, field
from time import perf_counter
from typing import Any

from providers.provider_factory import get_provider
from services.provider_cost_service import ProviderCostService


@dataclass
class ProviderConfiguration:
    provider_name: str
    model: str
    provider_options: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(frozen=True)
class ProviderComparisonResult:
    provider_name: str
    model: str
    response: str | None
    latency_ms: float
    success: bool
    error: str | None
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cached_input_tokens: int = 0
    reasoning_tokens: int = 0
    estimated_uncached_input_cost_usd: float | None = None
    estimated_cached_input_cost_usd: float | None = None
    estimated_output_cost_usd: float | None = None
    estimated_total_cost_usd: float | None = None
    pricing_tier: str | None = None
    pricing_effective_date: str | None = None
    cost_error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class MultiProviderComparisonService:

    def __init__(
        self,
        clock: Callable[[], float] = perf_counter,
        cost_service: ProviderCostService | None = None
    ):
        self._clock = clock
        self._cost_service = (
            cost_service or ProviderCostService()
        )

    def compare(
        self,
        prompt: str,
        providers: Sequence[ProviderConfiguration]
    ) -> list[ProviderComparisonResult]:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        if not providers:
            raise ValueError(
                "At least one provider must be configured."
            )

        return [
            self._execute_provider(prompt, configuration)
            for configuration in providers
        ]

    def _execute_provider(
        self,
        prompt: str,
        configuration: ProviderConfiguration
    ) -> ProviderComparisonResult:
        started_at = self._clock()

        try:
            provider = get_provider(
                provider_name=configuration.provider_name,
                model=configuration.model,
                **configuration.provider_options
            )

            generation = provider.generate_response_with_usage(
                prompt
            )

            response = generation.text
            success = True
            error = None
            input_tokens = generation.input_tokens
            output_tokens = generation.output_tokens
            total_tokens = generation.total_tokens
            cached_input_tokens = (
                generation.cached_input_tokens
            )
            reasoning_tokens = generation.reasoning_tokens

            cost_fields = self._estimate_cost(
                configuration=configuration,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cached_input_tokens=cached_input_tokens
            )

        except Exception as exception:
            response = None
            success = False
            error = (
                f"{type(exception).__name__}: "
                f"{exception}"
            )
            input_tokens = 0
            output_tokens = 0
            total_tokens = 0
            cached_input_tokens = 0
            reasoning_tokens = 0
            cost_fields = self._empty_cost_fields()

        latency_ms = round(
            (self._clock() - started_at) * 1000,
            2
        )

        return ProviderComparisonResult(
            provider_name=configuration.provider_name,
            model=configuration.model,
            response=response,
            latency_ms=latency_ms,
            success=success,
            error=error,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            cached_input_tokens=cached_input_tokens,
            reasoning_tokens=reasoning_tokens,
            **cost_fields
        )

    def _estimate_cost(
        self,
        configuration: ProviderConfiguration,
        input_tokens: int,
        output_tokens: int,
        cached_input_tokens: int
    ) -> dict[str, Any]:
        try:
            estimate = self._cost_service.estimate(
                provider_name=configuration.provider_name,
                model=configuration.model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cached_input_tokens=cached_input_tokens
            )

            return {
                "estimated_uncached_input_cost_usd": float(
                    estimate.uncached_input_cost_usd
                ),
                "estimated_cached_input_cost_usd": float(
                    estimate.cached_input_cost_usd
                ),
                "estimated_output_cost_usd": float(
                    estimate.output_cost_usd
                ),
                "estimated_total_cost_usd": float(
                    estimate.total_cost_usd
                ),
                "pricing_tier": estimate.pricing_tier,
                "pricing_effective_date": (
                    estimate.pricing_effective_date
                ),
                "cost_error": None
            }

        except Exception as exception:
            return {
                **self._empty_cost_fields(),
                "cost_error": (
                    f"{type(exception).__name__}: "
                    f"{exception}"
                )
            }

    @staticmethod
    def _empty_cost_fields() -> dict[str, Any]:
        return {
            "estimated_uncached_input_cost_usd": None,
            "estimated_cached_input_cost_usd": None,
            "estimated_output_cost_usd": None,
            "estimated_total_cost_usd": None,
            "pricing_tier": None,
            "pricing_effective_date": None,
            "cost_error": None
        }