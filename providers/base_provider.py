from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass