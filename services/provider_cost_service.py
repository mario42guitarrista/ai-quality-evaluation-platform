from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from config.provider_pricing import get_model_pricing


TOKENS_PER_MILLION = Decimal("1000000")
COST_PRECISION = Decimal("0.000000000001")


@dataclass(frozen=True)
class ProviderCostEstimate:
    provider_name: str
    model: str
    pricing_tier: str
    pricing_effective_date: str
    input_tokens: int
    cached_input_tokens: int
    uncached_input_tokens: int
    output_tokens: int
    uncached_input_cost_usd: Decimal
    cached_input_cost_usd: Decimal
    output_cost_usd: Decimal
    total_cost_usd: Decimal

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider_name": self.provider_name,
            "model": self.model,
            "pricing_tier": self.pricing_tier,
            "pricing_effective_date": (
                self.pricing_effective_date
            ),
            "input_tokens": self.input_tokens,
            "cached_input_tokens": (
                self.cached_input_tokens
            ),
            "uncached_input_tokens": (
                self.uncached_input_tokens
            ),
            "output_tokens": self.output_tokens,
            "uncached_input_cost_usd": float(
                self.uncached_input_cost_usd
            ),
            "cached_input_cost_usd": float(
                self.cached_input_cost_usd
            ),
            "output_cost_usd": float(
                self.output_cost_usd
            ),
            "total_cost_usd": float(
                self.total_cost_usd
            )
        }


class ProviderCostService:

    def estimate(
        self,
        provider_name: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        cached_input_tokens: int = 0
    ) -> ProviderCostEstimate:
        self._validate_token_counts(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cached_input_tokens=cached_input_tokens
        )

        pricing = get_model_pricing(
            provider_name=provider_name,
            model=model
        )

        uncached_input_tokens = (
            input_tokens - cached_input_tokens
        )

        uncached_input_cost = self._calculate_cost(
            tokens=uncached_input_tokens,
            price_per_million=(
                pricing.input_per_million_usd
            )
        )

        cached_input_cost = self._calculate_cost(
            tokens=cached_input_tokens,
            price_per_million=(
                pricing.cached_input_per_million_usd
            )
        )

        output_cost = self._calculate_cost(
            tokens=output_tokens,
            price_per_million=(
                pricing.output_per_million_usd
            )
        )

        total_cost = (
            uncached_input_cost
            + cached_input_cost
            + output_cost
        ).quantize(COST_PRECISION)

        return ProviderCostEstimate(
            provider_name=pricing.provider_name,
            model=pricing.model,
            pricing_tier=pricing.pricing_tier,
            pricing_effective_date=pricing.effective_date,
            input_tokens=input_tokens,
            cached_input_tokens=cached_input_tokens,
            uncached_input_tokens=uncached_input_tokens,
            output_tokens=output_tokens,
            uncached_input_cost_usd=uncached_input_cost,
            cached_input_cost_usd=cached_input_cost,
            output_cost_usd=output_cost,
            total_cost_usd=total_cost
        )

    @staticmethod
    def _calculate_cost(
        tokens: int,
        price_per_million: Decimal
    ) -> Decimal:
        return (
            Decimal(tokens)
            * price_per_million
            / TOKENS_PER_MILLION
        ).quantize(COST_PRECISION)

    @staticmethod
    def _validate_token_counts(
        input_tokens: int,
        output_tokens: int,
        cached_input_tokens: int
    ) -> None:
        if (
            input_tokens < 0
            or output_tokens < 0
            or cached_input_tokens < 0
        ):
            raise ValueError(
                "Token counts cannot be negative."
            )

        if cached_input_tokens > input_tokens:
            raise ValueError(
                "Cached input tokens cannot exceed "
                "total input tokens."
            )