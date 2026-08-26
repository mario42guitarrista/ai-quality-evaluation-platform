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

    def __init__(self, results_by_run):
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

    if success and provider_name == "openai":
        input_tokens = 100
        output_tokens = 20
        total_tokens = 120
        cached_input_tokens = 10
        reasoning_tokens = 5
        uncached_input_cost = 0.000036
        cached_input_cost = 0.000001
        output_cost = 0.000032
        total_cost = 0.000069
        pricing_tier = "standard_paid"
        pricing_effective_date = "2026-08-20"

    elif success:
        input_tokens = 80
        output_tokens = 30
        total_tokens = 110
        cached_input_tokens = 5
        reasoning_tokens = 10
        uncached_input_cost = 0.0000225
        cached_input_cost = 0.00000015
        output_cost = 0.000075
        total_cost = 0.00009765
        pricing_tier = "standard_paid"
        pricing_effective_date = "2026-08-20"

    else:
        input_tokens = 0
        output_tokens = 0
        total_tokens = 0
        cached_input_tokens = 0
        reasoning_tokens = 0
        uncached_input_cost = None
        cached_input_cost = None
        output_cost = None
        total_cost = None
        pricing_tier = None
        pricing_effective_date = None

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
        ),
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        cached_input_tokens=cached_input_tokens,
        reasoning_tokens=reasoning_tokens,
        estimated_uncached_input_cost_usd=(
            uncached_input_cost
        ),
        estimated_cached_input_cost_usd=(
            cached_input_cost
        ),
        estimated_output_cost_usd=output_cost,
        estimated_total_cost_usd=total_cost,
        pricing_tier=pricing_tier,
        pricing_effective_date=(
            pricing_effective_date
        )
    )


def test_benchmark_aggregates_latency_failures_and_costs():
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
    assert openai.total_input_tokens == 300
    assert openai.total_output_tokens == 60
    assert openai.total_tokens == 360
    assert openai.total_cached_input_tokens == 30
    assert openai.total_reasoning_tokens == 15
    assert openai.priced_runs == 3
    assert openai.unpriced_successful_runs == 0
    assert openai.estimated_total_cost_usd == 0.000207
    assert (
        openai.estimated_average_cost_per_run_usd
        == 0.000069
    )
    assert openai.pricing_tier == "standard_paid"
    assert openai.pricing_effective_date == "2026-08-20"

    gemini = summaries["gemini"]

    assert gemini.total_runs == 3
    assert gemini.successful_runs == 2
    assert gemini.failed_runs == 1
    assert gemini.success_rate_percent == 66.67
    assert gemini.minimum_latency_ms == 200.0
    assert gemini.maximum_latency_ms == 300.0
    assert gemini.average_latency_ms == 250.0
    assert gemini.median_latency_ms == 250.0
    assert gemini.total_input_tokens == 160
    assert gemini.total_output_tokens == 60
    assert gemini.total_tokens == 220
    assert gemini.total_cached_input_tokens == 10
    assert gemini.total_reasoning_tokens == 20
    assert gemini.priced_runs == 2
    assert gemini.unpriced_successful_runs == 0
    assert gemini.estimated_total_cost_usd == 0.0001953
    assert (
        gemini.estimated_average_cost_per_run_usd
        == 0.00009765
    )

    payload = report.to_dict()

    assert payload["requested_runs"] == 3
    assert (
        payload["summaries"][0]
        ["estimated_total_cost_usd"]
        == 0.000207
    )


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
    assert summary.total_input_tokens == 0
    assert summary.total_output_tokens == 0
    assert summary.total_tokens == 0
    assert summary.priced_runs == 0
    assert summary.estimated_total_cost_usd is None
    assert (
        summary.estimated_average_cost_per_run_usd
        is None
    )


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