from openai import OpenAI
from dotenv import load_dotenv
import os

from providers.base_provider import BaseLLMProvider


load_dotenv()


class OpenAIProvider(BaseLLMProvider):

    def __init__(self, model: str = "gpt-4.1-mini"):
        self.model = model
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

    def generate_response(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content