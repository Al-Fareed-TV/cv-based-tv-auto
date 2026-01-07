import os
from PIL import Image
import base64
import io
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None
from .base import LLMProvider

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str = None, model: str = None):
        if OpenAI is None:
             raise ImportError("The 'openai' library is not installed. Please run `pip install openai`.")
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        # OpenAI provider is optional, so we don't strict raise if not present unless used
        
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def _encode_image(self, image: Image.Image) -> str:
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def generate_content(self, prompt: str, image: Image.Image) -> str:
        if not self.client:
             raise RuntimeError("OPENAI_API_KEY not set")

        base64_image = self._encode_image(image)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=300,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI generation failed: {e}") from e

    def generate_text(self, prompt: str) -> str:
        if not self.client:
             raise RuntimeError("OPENAI_API_KEY not set")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                max_tokens=300,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI text generation failed: {e}") from e
