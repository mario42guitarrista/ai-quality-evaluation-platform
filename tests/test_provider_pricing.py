from decimal import Decimal

import pytest

from config.provider_pricing import get_model_pricing


def test_get_openai_pricing():
    pricing = get_model_pricing(
        provider_name="openai",
        model="gpt-4.1-mini"
    )

    assert pricing.input_per_million_usd == Decimal("0.40")
    assert (
        pricing.cached_input_per_million_usd
        == Decimal("0.10")
    )
    assert pricing.output_per_million_usd == Decimal("1.60")
    assert pricing.pricing_tier == "standard_paid"
    assert pricing.effective_date == "2026-08-20"


def test_get_gemini_pricing():
    pricing = get_model_pricing(
        provider_name="gemini",
        model="gemini-3.5-flash-lite"
    )

    assert pricing.input_per_million_usd == Decimal("0.30")
    assert (
        pricing.cached_input_per_million_usd
        == Decimal("0.03")
    )
    assert pricing.output_per_million_usd == Decimal("2.50")


def test_provider_name_is_case_insensitive():
    pricing = get_model_pricing(
        provider_name="OpenAI",
        model="gpt-4.1-mini"
    )

    assert pricing.provider_name == "openai"


@pytest.mark.parametrize(
    (
        "provider_name",
        "model",
        "expected_message"
    ),
    [
        (
            "",
            "gpt-4.1-mini",
            "Provider name cannot be empty"
        ),
        (
            "openai",
            "",
            "Model cannot be empty"
        ),
        (
            "unknown",
            "unknown-model",
            "Pricing is not configured"
        )
    ]
)
def test_get_model_pricing_rejects_invalid_configuration(
    provider_name,
    model,
    expected_message
):
    with pytest.raises(
        ValueError,
        match=expected_message
    ):
        get_model_pricing(
            provider_name=provider_name,
            model=model
        )