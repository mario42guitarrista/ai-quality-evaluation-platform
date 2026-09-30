from typing import Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class ProviderConfigurationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider_name: str = Field(min_length=1)
    model: str = Field(min_length=1)
    provider_options: dict[str, Any] = Field(
        default_factory=dict
    )

    @field_validator("provider_name", "model")
    @classmethod
    def reject_blank_values(cls, value: str) -> str:
        normalized_value = value.strip()

        if not normalized_value:
            raise ValueError(
                "Provider name and model cannot be empty."
            )

        return normalized_value


class ProviderComparisonRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt: str = Field(min_length=1)
    providers: list[ProviderConfigurationRequest] = Field(
        min_length=1
    )

    @field_validator("prompt")
    @classmethod
    def reject_blank_prompt(cls, value: str) -> str:
        normalized_prompt = value.strip()

        if not normalized_prompt:
            raise ValueError("Prompt cannot be empty.")

        return normalized_prompt


class ProviderComparisonResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    provider_name: str
    model: str
    response: str | None
    latency_ms: float
    success: bool
    error: str | None
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cached_input_tokens: int
    reasoning_tokens: int
    estimated_uncached_input_cost_usd: float | None
    estimated_cached_input_cost_usd: float | None
    estimated_output_cost_usd: float | None
    estimated_total_cost_usd: float | None
    pricing_tier: str | None
    pricing_effective_date: str | None
    cost_error: str | None


class ProviderComparisonResponse(BaseModel):
    prompt: str
    results: list[ProviderComparisonResultResponse]