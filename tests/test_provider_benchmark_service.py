import pytest

from services.provider_benchmark_service import (
    MultiRunProviderBenchmarkService,
)
from services.provider_comparison_service import (
    ProviderComparisonResult,
    ProviderConfiguration,
)


CONFIGURATIONS = [
    ProviderConfiguration(
        provider_name="openai",
        model="gpt-test"
    ),
    ProviderConfiguration(
        provider_name="gemini",
        model="gemini-test"
    )
]


class StubComparisonService:

    def __init__(
        self,
        results_by_run: list[
            list[ProviderComparisonResult]
        ]
    ):
        self._results_by_run = iter(results_by_run)

    def compare(
        self,
        prompt,
        providers
    ) -> list[ProviderComparisonResult]:
        return next(self._results_by_run)


def create_result(
    provider_name: str,
    latency_ms: float,
    success: bool = True
) -> ProviderComparisonResult:
    model = (
        "gpt-test"
        if provider_name == "openai"
        else "gemini-test"
    )

    return ProviderComparisonResult(
        provider_name=provider_name,
        model=model,
        response=(
            f"{provider_name} response"
            if success
            else None
        ),
        latency_ms=latency_ms,
        success=success,
        error=(
            None
            if success
            else "RuntimeError: Provider unavailable"
        )
    )


def test_benchmark_aggregates_latency_and_failures():
    comparison_service = StubComparisonService([
        [
            create_result("openai", 100.0),
            create_result("gemini", 200.0)
        ],
        [
            create_result("openai", 150.0),
            create_result(
                "gemini",
                50.0,
                success=False
            )
        ],
        [
            create_result("openai", 200.0),
            create_result("gemini", 300.0)
        ]
    ])

    service = MultiRunProviderBenchmarkService(
        comparison_service=comparison_service
    )

    report = service.benchmark(
        prompt="Explain regression testing.",
        providers=CONFIGURATIONS,
        runs=3
    )

    assert report.requested_runs == 3
    assert len(report.results) == 6

    assert [
        result.run_number
        for result in report.results
    ] == [1, 1, 2, 2, 3, 3]

    summaries = {
        summary.provider_name: summary
        for summary in report.summaries
    }

    openai = summaries["openai"]

    assert openai.total_runs == 3
    assert openai.successful_runs == 3
    assert openai.failed_runs == 0
    assert openai.success_rate_percent == 100.0
    assert openai.minimum_latency_ms == 100.0
    assert openai.maximum_latency_ms == 200.0
    assert openai.average_latency_ms == 150.0
    assert openai.median_latency_ms == 150.0

    gemini = summaries["gemini"]

    assert gemini.total_runs == 3
    assert gemini.successful_runs == 2
    assert gemini.failed_runs == 1
    assert gemini.success_rate_percent == 66.67
    assert gemini.minimum_latency_ms == 200.0
    assert gemini.maximum_latency_ms == 300.0
    assert gemini.average_latency_ms == 250.0
    assert gemini.median_latency_ms == 250.0

    assert report.to_dict()["requested_runs"] == 3


def test_benchmark_uses_none_when_all_runs_fail():
    comparison_service = StubComparisonService([
        [
            create_result(
                "gemini",
                10.0,
                success=False
            )
        ],
        [
            create_result(
                "gemini",
                20.0,
                success=False
            )
        ]
    ])

    service = MultiRunProviderBenchmarkService(
        comparison_service=comparison_service
    )

    report = service.benchmark(
        prompt="Explain smoke testing.",
        providers=[CONFIGURATIONS[1]],
        runs=2
    )

    summary = report.summaries[0]

    assert summary.total_runs == 2
    assert summary.successful_runs == 0
    assert summary.failed_runs == 2
    assert summary.success_rate_percent == 0.0
    assert summary.minimum_latency_ms is None
    assert summary.maximum_latency_ms is None
    assert summary.average_latency_ms is None
    assert summary.median_latency_ms is None


@pytest.mark.parametrize(
    (
        "prompt",
        "providers",
        "runs",
        "expected_message"
    ),
    [
        (
            " ",
            CONFIGURATIONS,
            3,
            "Prompt cannot be empty"
        ),
        (
            "Explain API testing.",
            [],
            3,
            "At least one provider"
        ),
        (
            "Explain API testing.",
            CONFIGURATIONS,
            0,
            "Runs must be greater"
        )
    ]
)
def test_benchmark_rejects_invalid_inputs(
    prompt,
    providers,
    runs,
    expected_message
):
    service = MultiRunProviderBenchmarkService(
        comparison_service=StubComparisonService([])
    )

    with pytest.raises(
        ValueError,
        match=expected_message
    ):
        service.benchmark(
            prompt=prompt,
            providers=providers,
            runs=runs
        )