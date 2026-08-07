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
            f"{result.latency_ms} ms | "
            f"{status}"
        )

        if result.response:
            print(f"Response: {result.response}")

        if result.error:
            print(f"Error: {result.error}")

        print()

    print(f"Report saved to: {report_path}")

    if not all(result.success for result in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()