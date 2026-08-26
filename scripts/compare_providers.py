import json
from datetime import datetime, timezone
from pathlib import Path

from services.provider_comparison_service import (
    MultiProviderComparisonService,
    ProviderConfiguration,
)


PROMPT = (
    "Explain the purpose of regression testing "
    "in one concise sentence."
)

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
    "reports/provider_comparisons"
)


def format_cost(
    cost_usd: float | None
) -> str:
    if cost_usd is None:
        return "N/A"

    return f"${cost_usd:.8f}"


def main() -> None:
    comparison_service = MultiProviderComparisonService()

    results = comparison_service.compare(
        prompt=PROMPT,
        providers=PROVIDERS
    )

    report = {
        "generated_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "prompt": PROMPT,
        "results": [
            result.to_dict()
            for result in results
        ]
    }

    REPORT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    report_path = REPORT_DIRECTORY / (
        "provider_comparison.json"
    )

    report_path.write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    print("\nMulti-Provider Comparison\n")

    for result in results:
        status = (
            "SUCCESS"
            if result.success
            else "FAILED"
        )

        print(
            f"{result.provider_name.upper()} | "
            f"{result.model} | "
            f"{result.latency_ms:.2f} ms | "
            f"{status}"
        )

        if result.response:
            print(f"Response: {result.response}")

        if result.success:
            print(
                "Tokens: "
                f"input={result.input_tokens} | "
                f"cached={result.cached_input_tokens} | "
                f"output={result.output_tokens} | "
                f"reasoning={result.reasoning_tokens} | "
                f"total={result.total_tokens}"
            )

            uncached_input_cost = format_cost(
                result.estimated_uncached_input_cost_usd
            )
            cached_input_cost = format_cost(
                result.estimated_cached_input_cost_usd
            )
            output_cost = format_cost(
                result.estimated_output_cost_usd
            )
            total_cost = format_cost(
                result.estimated_total_cost_usd
            )

            print(
                "Estimated cost: "
                f"input={uncached_input_cost} | "
                f"cached={cached_input_cost} | "
                f"output={output_cost} | "
                f"total={total_cost}"
            )

            if result.pricing_tier:
                print(
                    "Pricing: "
                    f"tier={result.pricing_tier} | "
                    "effective date="
                    f"{result.pricing_effective_date}"
                )

            if result.cost_error:
                print(
                    f"Cost warning: {result.cost_error}"
                )

        if result.error:
            print(f"Error: {result.error}")

        print()

    print(f"Report saved to: {report_path}")

    if not all(result.success for result in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()