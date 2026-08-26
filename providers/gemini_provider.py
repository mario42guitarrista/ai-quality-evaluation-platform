import os
from typing import Any

from dotenv import load_dotenv
from google import genai

from providers.base_provider import (
    BaseLLMProvider,
    ProviderGenerationResult,
)


load_dotenv()


class GeminiProvider(BaseLLMProvider):

    def __init__(
        self,
        model: str = "gemini-3.5-flash-lite",
        api_key: str | None = None,
        client: Any | None = None
    ):
        self.model = model

        if client is not None:
            self.client = client
            return

        resolved_api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not resolved_api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not configured."
            )

        self.client = genai.Client(api_key=resolved_api_key)

    def generate_response(self, prompt: str) -> str:
        return self.generate_response_with_usage(prompt).text

    def generate_response_with_usage(
        self,
        prompt: str
    ) -> ProviderGenerationResult:
        interaction = self.client.interactions.create(
            model=self.model,
            input=prompt,
            store=False
        )

        response_text = interaction.output_text

        if not response_text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        usage = getattr(interaction, "usage", None)

        input_tokens = int(
            getattr(usage, "total_input_tokens", 0) or 0
        )
        generated_output_tokens = int(
            getattr(usage, "total_output_tokens", 0) or 0
        )
        reasoning_tokens = int(
            getattr(usage, "total_thought_tokens", 0) or 0
        )

        return ProviderGenerationResult(
            text=response_text,
            input_tokens=input_tokens,
            output_tokens=(
                generated_output_tokens
                + reasoning_tokens
            ),
            total_tokens=int(
                getattr(usage, "total_tokens", 0) or 0
            ),
            cached_input_tokens=int(
                getattr(
                    usage,
                    "total_cached_tokens",
                    0
                ) or 0
            ),
            reasoning_tokens=reasoning_tokens
        )