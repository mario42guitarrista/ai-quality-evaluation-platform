from collections.abc import Sequence
from dataclasses import asdict, dataclass
from statistics import mean, median
from typing import Any, Protocol

from services.provider_comparison_service import (
    MultiProviderComparisonService,
    ProviderComparisonResult,
    ProviderConfiguration,
)


class ProviderComparisonRunner(Protocol):

    def compare(
        self,
        prompt: str,
        providers: Sequence[ProviderConfiguration]
    ) -> list[ProviderComparisonResult]:
        ...


@dataclass(frozen=True)
class ProviderBenchmarkRunResult:
    run_number: int
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


@dataclass(frozen=True)
class ProviderBenchmarkSummary:
    provider_name: str
    model: str
    total_runs: int
    successful_runs: int
    failed_runs: int
    success_rate_percent: float
    minimum_latency_ms: float | None
    maximum_latency_ms: float | None
    average_latency_ms: float | None
    median_latency_ms: float | None
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_tokens: int = 0
    total_cached_input_tokens: int = 0
    total_reasoning_tokens: int = 0
    priced_runs: int = 0
    unpriced_successful_runs: int = 0
    estimated_total_cost_usd: float | None = None
    estimated_average_cost_per_run_usd: float | None = None
    pricing_tier: str | None = None
    pricing_effective_date: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProviderBenchmarkReport:
    prompt: str
    requested_runs: int
    results: list[ProviderBenchmarkRunResult]
    summaries: list[ProviderBenchmarkSummary]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class MultiRunProviderBenchmarkService:

    def __init__(
        self,
        comparison_service: ProviderComparisonRunner | None = None
    ):
        self._comparison_service = (
            comparison_service
            or MultiProviderComparisonService()
        )

    def benchmark(
        self,
        prompt: str,
        providers: Sequence[ProviderConfiguration],
        runs: int = 3
    ) -> ProviderBenchmarkReport:
        self._validate_inputs(
            prompt=prompt,
            providers=providers,
            runs=runs
        )

        run_results: list[ProviderBenchmarkRunResult] = []

        for run_number in range(1, runs + 1):
            comparison_results = (
                self._comparison_service.compare(
                    prompt=prompt,
                    providers=providers
                )
            )

            for result in comparison_results:
                run_results.append(
                    ProviderBenchmarkRunResult(
                        run_number=run_number,
                        provider_name=result.provider_name,
                        model=result.model,
                        response=result.response,
                        latency_ms=result.latency_ms,
                        success=result.success,
                        error=result.error,
                        input_tokens=result.input_tokens,
                        output_tokens=result.output_tokens,
                        total_tokens=result.total_tokens,
                        cached_input_tokens=(
                            result.cached_input_tokens
                        ),
                        reasoning_tokens=(
                            result.reasoning_tokens
                        ),
                        estimated_uncached_input_cost_usd=(
                            result
                            .estimated_uncached_input_cost_usd
                        ),
                        estimated_cached_input_cost_usd=(
                            result
                            .estimated_cached_input_cost_usd
                        ),
                        estimated_output_cost_usd=(
                            result.estimated_output_cost_usd
                        ),
                        estimated_total_cost_usd=(
                            result.estimated_total_cost_usd
                        ),
                        pricing_tier=result.pricing_tier,
                        pricing_effective_date=(
                            result.pricing_effective_date
                        ),
                        cost_error=result.cost_error
                    )
                )

        summaries = [
            self._create_summary(
                configuration=configuration,
                run_results=run_results
            )
            for configuration in providers
        ]

        return ProviderBenchmarkReport(
            prompt=prompt,
            requested_runs=runs,
            results=run_results,
            summaries=summaries
        )

    @staticmethod
    def _validate_inputs(
        prompt: str,
        providers: Sequence[ProviderConfiguration],
        runs: int
    ) -> None:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        if not providers:
            raise ValueError(
                "At least one provider must be configured."
            )

        if runs < 1:
            raise ValueError(
                "Runs must be greater than or equal to 1."
            )

    @classmethod
    def _create_summary(
        cls,
        configuration: ProviderConfiguration,
        run_results: Sequence[ProviderBenchmarkRunResult]
    ) -> ProviderBenchmarkSummary:
        provider_results = [
            result
            for result in run_results
            if (
                result.provider_name
                == configuration.provider_name
                and result.model == configuration.model
            )
        ]

        successful_results = [
            result
            for result in provider_results
            if result.success
        ]

        successful_latencies = [
            result.latency_ms
            for result in successful_results
        ]

        priced_results = [
            result
            for result in successful_results
            if result.estimated_total_cost_usd is not None
        ]

        estimated_costs = [
            result.estimated_total_cost_usd
            for result in priced_results
            if result.estimated_total_cost_usd is not None
        ]

        total_runs = len(provider_results)
        successful_runs = len(successful_results)
        failed_runs = total_runs - successful_runs
        priced_runs = len(priced_results)

        success_rate_percent = (
            round(
                successful_runs / total_runs * 100,
                2
            )
            if total_runs
            else 0.0
        )

        if successful_latencies:
            minimum_latency_ms = round(
                min(successful_latencies),
                2
            )
            maximum_latency_ms = round(
                max(successful_latencies),
                2
            )
            average_latency_ms = round(
                mean(successful_latencies),
                2
            )
            median_latency_ms = round(
                median(successful_latencies),
                2
            )
        else:
            minimum_latency_ms = None
            maximum_latency_ms = None
            average_latency_ms = None
            median_latency_ms = None

        if estimated_costs:
            estimated_total_cost_usd = round(
                sum(estimated_costs),
                12
            )
            estimated_average_cost_per_run_usd = round(
                mean(estimated_costs),
                12
            )
        else:
            estimated_total_cost_usd = None
            estimated_average_cost_per_run_usd = None

        pricing_tier = cls._single_or_mixed(
            {
                result.pricing_tier
                for result in priced_results
                if result.pricing_tier is not None
            }
        )

        pricing_effective_date = cls._single_or_mixed(
            {
                result.pricing_effective_date
                for result in priced_results
                if result.pricing_effective_date is not None
            }
        )

        return ProviderBenchmarkSummary(
            provider_name=configuration.provider_name,
            model=configuration.model,
            total_runs=total_runs,
            successful_runs=successful_runs,
            failed_runs=failed_runs,
            success_rate_percent=success_rate_percent,
            minimum_latency_ms=minimum_latency_ms,
            maximum_latency_ms=maximum_latency_ms,
            average_latency_ms=average_latency_ms,
            median_latency_ms=median_latency_ms,
            total_input_tokens=sum(
                result.input_tokens
                for result in successful_results
            ),
            total_output_tokens=sum(
                result.output_tokens
                for result in successful_results
            ),
            total_tokens=sum(
                result.total_tokens
                for result in successful_results
            ),
            total_cached_input_tokens=sum(
                result.cached_input_tokens
                for result in successful_results
            ),
            total_reasoning_tokens=sum(
                result.reasoning_tokens
                for result in successful_results
            ),
            priced_runs=priced_runs,
            unpriced_successful_runs=(
                successful_runs - priced_runs
            ),
            estimated_total_cost_usd=(
                estimated_total_cost_usd
            ),
            estimated_average_cost_per_run_usd=(
                estimated_average_cost_per_run_usd
            ),
            pricing_tier=pricing_tier,
            pricing_effective_date=(
                pricing_effective_date
            )
        )

    @staticmethod
    def _single_or_mixed(
        values: set[str]
    ) -> str | None:
        if not values:
            return None

        if len(values) == 1:
            return next(iter(values))

        return "mixed"