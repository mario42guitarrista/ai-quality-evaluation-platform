import json
from datetime import datetime, timezone
from pathlib import Path

from services.provider_benchmark_service import (
    MultiRunProviderBenchmarkService,
)
from services.provider_comparison_service import (
    ProviderConfiguration,
)


PROMPT = (
    "Explain the purpose of regression testing "
    "in one concise sentence."
)

RUNS = 3

PROVIDERS = [
    ProviderConfiguration(
        provider_name="openai",
        model="gpt-4.1-mini"
    ),
    ProviderConfiguration(
        provider_name="gemini",
        model="gemini-3.5-flash-lite"
    )
]

REPORT_DIRECTORY = Path(
    "reports/provider_benchmarks"
)


def format_latency(
    latency_ms: float | None
) -> str:
    if latency_ms is None:
        return "N/A"

    return f"{latency_ms:.2f} ms"


def format_cost(
    cost_usd: float | None
) -> str:
    if cost_usd is None:
        return "N/A"

    return f"${cost_usd:.8f}"


def main() -> None:
    benchmark_service = (
        MultiRunProviderBenchmarkService()
    )

    report = benchmark_service.benchmark(
        prompt=PROMPT,
        providers=PROVIDERS,
        runs=RUNS
    )

    report_payload = {
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        **report.to_dict()
    }

    REPORT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    report_path = REPORT_DIRECTORY / (
        "provider_benchmark.json"
    )

    report_path.write_text(
        json.dumps(
            report_payload,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    print("\nMulti-Run Provider Benchmark\n")
    print(
        f"Runs per provider: "
        f"{report.requested_runs}\n"
    )

    for summary in report.summaries:
        print(
            f"{summary.provider_name.upper()} | "
            f"{summary.model}"
        )

        print(
            "Success: "
            f"{summary.successful_runs}/"
            f"{summary.total_runs} "
            f"({summary.success_rate_percent:.2f}%)"
        )

        print(
            "Latency: "
            f"min={format_latency(summary.minimum_latency_ms)} | "
            f"avg={format_latency(summary.average_latency_ms)} | "
            f"median={format_latency(summary.median_latency_ms)} | "
            f"max={format_latency(summary.maximum_latency_ms)}"
        )

        print(
            "Tokens: "
            f"input={summary.total_input_tokens} | "
            f"cached={summary.total_cached_input_tokens} | "
            f"output={summary.total_output_tokens} | "
            f"reasoning={summary.total_reasoning_tokens} | "
            f"total={summary.total_tokens}"
        )

        total_cost = format_cost(
            summary.estimated_total_cost_usd
        )
        average_cost = format_cost(
            summary.estimated_average_cost_per_run_usd
        )

        print(
            "Estimated cost: "
            f"total={total_cost} | "
            f"average/run={average_cost} | "
            f"priced runs={summary.priced_runs}/"
            f"{summary.successful_runs}"
        )

        if summary.pricing_tier:
            print(
                "Pricing: "
                f"tier={summary.pricing_tier} | "
                "effective date="
                f"{summary.pricing_effective_date}"
            )

        print()

    print(f"Report saved to: {report_path}")

    if any(
        summary.failed_runs > 0
        for summary in report.summaries
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()