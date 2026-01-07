import os
from PIL import Image
from google import genai
from .base import LLMProvider

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY not set")
        
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        self.client = genai.Client(api_key=self.api_key)

    def generate_content(self, prompt: str, image: Image.Image) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt, image]
            )
            return response.text.strip()
        except Exception as e:
            raise RuntimeError(f"Gemini generation failed: {e}") from e

    def generate_text(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt]
            )
            return response.text.strip()
        except Exception as e:
            raise RuntimeError(f"Gemini text generation failed: {e}") from e
