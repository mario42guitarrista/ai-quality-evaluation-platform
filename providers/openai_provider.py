import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from providers.base_provider import (
    BaseLLMProvider,
    ProviderGenerationResult,
)


load_dotenv()


class OpenAIProvider(BaseLLMProvider):

    def __init__(
        self,
        model: str = "gpt-4.1-mini",
        api_key: str | None = None,
        client: Any | None = None
    ):
        self.model = model

        if client is not None:
            self.client = client
            return

        self.client = OpenAI(
            api_key=api_key or os.getenv("OPENAI_API_KEY")
        )

    def generate_response(self, prompt: str) -> str:
        return self.generate_response_with_usage(prompt).text

    def generate_response_with_usage(
        self,
        prompt: str
    ) -> ProviderGenerationResult:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        response_text = response.choices[0].message.content

        if not response_text:
            raise RuntimeError(
                "OpenAI returned an empty response."
            )

        usage = getattr(response, "usage", None)
        prompt_details = getattr(
            usage,
            "prompt_tokens_details",
            None
        )
        completion_details = getattr(
            usage,
            "completion_tokens_details",
            None
        )

        return ProviderGenerationResult(
            text=response_text,
            input_tokens=int(
                getattr(usage, "prompt_tokens", 0) or 0
            ),
            output_tokens=int(
                getattr(usage, "completion_tokens", 0) or 0
            ),
            total_tokens=int(
                getattr(usage, "total_tokens", 0) or 0
            ),
            cached_input_tokens=int(
                getattr(
                    prompt_details,
                    "cached_tokens",
                    0
                ) or 0
            ),
            reasoning_tokens=int(
                getattr(
                    completion_details,
                    "reasoning_tokens",
                    0
                ) or 0
            )
        )