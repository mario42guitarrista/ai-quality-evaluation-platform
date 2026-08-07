from collections.abc import Callable, Sequence
from dataclasses import asdict, dataclass, field
from time import perf_counter
from typing import Any

from providers.provider_factory import get_provider


@dataclass
class ProviderConfiguration:
    provider_name: str
    model: str
    provider_options: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass(frozen=True)
class ProviderComparisonResult:
    provider_name: str
    model: str
    response: str | None
    latency_ms: float
    success: bool
    error: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class MultiProviderComparisonService:

    def __init__(
        self,
        clock: Callable[[], float] = perf_counter
    ):
        self._clock = clock

    def compare(
        self,
        prompt: str,
        providers: Sequence[ProviderConfiguration]
    ) -> list[ProviderComparisonResult]:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        if not providers:
            raise ValueError(
                "At least one provider must be configured."
            )

        return [
            self._execute_provider(prompt, configuration)
            for configuration in providers
        ]

    def _execute_provider(
        self,
        prompt: str,
        configuration: ProviderConfiguration
    ) -> ProviderComparisonResult:
        started_at = self._clock()

        try:
            provider = get_provider(
                provider_name=configuration.provider_name,
                model=configuration.model,
                **configuration.provider_options
            )

            response = provider.generate_response(prompt)
            success = True
            error = None

        except Exception as exception:
            response = None
            success = False
            error = (
                f"{type(exception).__name__}: "
                f"{exception}"
            )

        latency_ms = round(
            (self._clock() - started_at) * 1000,
            2
        )

        return ProviderComparisonResult(
            provider_name=configuration.provider_name,
            model=configuration.model,
            response=response,
            latency_ms=latency_ms,
            success=success,
            error=error
        )