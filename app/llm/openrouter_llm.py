import os

from openai import OpenAI

from app.llm.base import BaseLLM


class OpenRouterLLM(BaseLLM):
    """
    OpenRouter implementation of BaseLLM.
    """

    def __init__(self):

        self.client = OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        )

        self.model = os.getenv(
            "OPENROUTER_MODEL",
            "openrouter/free",
            )

        print(f"Using OpenRouter model: {self.model}")

    def generate(self, prompt: str) -> str:

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],

            temperature=0.2,
        )

        return response.choices[0].message.content.strip()