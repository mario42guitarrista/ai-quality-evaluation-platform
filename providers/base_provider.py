from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ProviderGenerationResult:
    text: str
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cached_input_tokens: int = 0
    reasoning_tokens: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class BaseLLMProvider(ABC):

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass

    def generate_response_with_usage(
        self,
        prompt: str
    ) -> ProviderGenerationResult:
        return ProviderGenerationResult(
            text=self.generate_response(prompt)
        )