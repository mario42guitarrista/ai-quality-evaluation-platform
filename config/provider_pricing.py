from dataclasses import dataclass
from decimal import Decimal


PRICING_EFFECTIVE_DATE = "2026-08-20"


@dataclass(frozen=True)
class ModelPricing:
    provider_name: str
    model: str
    input_per_million_usd: Decimal
    cached_input_per_million_usd: Decimal
    output_per_million_usd: Decimal
    pricing_tier: str
    effective_date: str


MODEL_PRICING = {
    (
        "openai",
        "gpt-4.1-mini"
    ): ModelPricing(
        provider_name="openai",
        model="gpt-4.1-mini",
        input_per_million_usd=Decimal("0.40"),
        cached_input_per_million_usd=Decimal("0.10"),
        output_per_million_usd=Decimal("1.60"),
        pricing_tier="standard_paid",
        effective_date=PRICING_EFFECTIVE_DATE
    ),
    (
        "gemini",
        "gemini-3.5-flash-lite"
    ): ModelPricing(
        provider_name="gemini",
        model="gemini-3.5-flash-lite",
        input_per_million_usd=Decimal("0.30"),
        cached_input_per_million_usd=Decimal("0.03"),
        output_per_million_usd=Decimal("2.50"),
        pricing_tier="standard_paid",
        effective_date=PRICING_EFFECTIVE_DATE
    )
}


def get_model_pricing(
    provider_name: str,
    model: str
) -> ModelPricing:
    normalized_provider = provider_name.strip().lower()
    normalized_model = model.strip()

    if not normalized_provider:
        raise ValueError("Provider name cannot be empty.")

    if not normalized_model:
        raise ValueError("Model cannot be empty.")

    try:
        return MODEL_PRICING[
            normalized_provider,
            normalized_model
        ]
    except KeyError as exception:
        raise ValueError(
            "Pricing is not configured for "
            f"provider '{provider_name}' "
            f"and model '{model}'."
        ) from exception