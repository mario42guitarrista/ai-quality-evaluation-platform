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
                        error=result.error
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

    @staticmethod
    def _create_summary(
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

        total_runs = len(provider_results)
        successful_runs = len(successful_results)
        failed_runs = total_runs - successful_runs

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
            median_latency_ms=median_latency_ms
        )