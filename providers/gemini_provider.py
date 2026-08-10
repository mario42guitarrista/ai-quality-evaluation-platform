import os
from typing import Any

from dotenv import load_dotenv
from google import genai

from providers.base_provider import BaseLLMProvider


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

        return response_text