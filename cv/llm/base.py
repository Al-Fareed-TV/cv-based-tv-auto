from abc import ABC, abstractmethod
from typing import Dict, Any, List
from PIL import Image

class LLMProvider(ABC):
    @abstractmethod
    def generate_content(self, prompt: str, image: Image.Image) -> str:
        """
        Generates content from the LLM based on a text prompt and an image.

        Args:
            prompt: The text prompt to send to the LLM.
            image: The image object (PIL Image) to analyze.

        Returns:
            The text response from the LLM.
        """
        pass

    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        """
        Generates text from the LLM based on a text prompt only.

        Args:
            prompt: The text prompt to send to the LLM.

        Returns:
            The text response from the LLM.
        """
        pass
