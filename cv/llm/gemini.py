import os
import tempfile
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
        # Save frame temporarily as Gemini client expects image objects/paths sometimes depending on the SDK version,
        # but the current implementation in llm_focus_detector.py was saving to a temp file.
        # However, checking the SDK, it often accepts PIL images directly or bytes.
        # Let's try to maintain the pattern that was working or improve if possible.
        # The original code:
        #   with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        #       Image.fromarray(frame).save(tmp.name)
        #       image = Image.open(tmp.name)
        #   contents=[prompt, image]
        
        # The google.genai library generally accepts PIL images in the contents list.
        # We will pass the PIL image directly.
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt, image]
            )
            return response.text.strip()
        except Exception as e:
            # Wrap exception or log it? For now, let it propagate but perhaps add context
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
