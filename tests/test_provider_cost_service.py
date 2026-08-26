from decimal import Decimal

import pytest

from services.provider_cost_service import (
    ProviderCostService,
)


def test_estimates_openai_cost():
    service = ProviderCostService()

    estimate = service.estimate(
        provider_name="openai",
        model="gpt-4.1-mini",
        input_tokens=100,
        output_tokens=25,
        cached_input_tokens=20
    )

    assert estimate.uncached_input_tokens == 80
    assert (
        estimate.uncached_input_cost_usd
        == Decimal("0.000032")
    )
    assert (
        estimate.cached_input_cost_usd
        == Decimal("0.000002")
    )
    assert estimate.output_cost_usd == Decimal("0.000040")
    assert estimate.total_cost_usd == Decimal("0.000074")
    assert estimate.pricing_tier == "standard_paid"

    assert estimate.to_dict()["total_cost_usd"] == 0.000074


def test_estimates_gemini_cost():
    service = ProviderCostService()

    estimate = service.estimate(
        provider_name="gemini",
        model="gemini-3.5-flash-lite",
        input_tokens=80,
        output_tokens=30,
        cached_input_tokens=5
    )

    assert estimate.uncached_input_tokens == 75
    assert (
        estimate.uncached_input_cost_usd
        == Decimal("0.0000225")
    )
    assert (
        estimate.cached_input_cost_usd
        == Decimal("0.00000015")
    )
    assert estimate.output_cost_usd == Decimal("0.000075")
    assert (
        estimate.total_cost_usd
        == Decimal("0.00009765")
    )


@pytest.mark.parametrize(
    (
        "input_tokens",
        "output_tokens",
        "cached_input_tokens",
        "expected_message"
    ),
    [
        (
            -1,
            10,
            0,
            "Token counts cannot be negative"
        ),
        (
            10,
            -1,
            0,
            "Token counts cannot be negative"
        ),
        (
            10,
            5,
            -1,
            "Token counts cannot be negative"
        ),
        (
            10,
            5,
            11,
            "Cached input tokens cannot exceed"
        )
    ]
)
def test_rejects_invalid_token_counts(
    input_tokens,
    output_tokens,
    cached_input_tokens,
    expected_message
):
    service = ProviderCostService()

    with pytest.raises(
        ValueError,
        match=expected_message
    ):
        service.estimate(
            provider_name="openai",
            model="gpt-4.1-mini",
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cached_input_tokens=cached_input_tokens
        )