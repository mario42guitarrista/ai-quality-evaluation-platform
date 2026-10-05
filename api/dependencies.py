from collections.abc import Sequence
from typing import Protocol

from services.provider_comparison_service import (
    MultiProviderComparisonService,
    ProviderComparisonResult,
    ProviderConfiguration,
)


class ProviderComparisonRunner(Protocol):

    def compare(
        self,
        prompt: str,
        providers: Sequence[ProviderConfiguration]
    ) -> list[ProviderComparisonResult]:
        ...


def get_provider_comparison_service(
) -> ProviderComparisonRunner:
    return MultiProviderComparisonService()