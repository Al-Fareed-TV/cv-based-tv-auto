import os
from typing import List
from PIL import Image
from .base import LLMProvider
from .gemini import GeminiProvider
from .openai import OpenAIProvider

class LLMManager:
    def __init__(self, providers: List[LLMProvider] = None):
        if providers:
            self.providers = providers
        else:
            self.providers = []
            selected_provider = os.getenv("LLM_PROVIDER", "auto").lower()

            gemini_key = os.getenv("GEMINI_API_KEY")
            openai_key = os.getenv("OPENAI_API_KEY")

            # Helper to add Gemini
            def add_gemini():
                if gemini_key:
                    try:
                        self.providers.append(GeminiProvider(api_key=gemini_key))
                    except Exception as e:
                        print(f"[WARN] Failed to initialize Gemini: {e}")

            # Helper to add OpenAI
            def add_openai():
                if openai_key:
                    try:
                        self.providers.append(OpenAIProvider(api_key=openai_key))
                    except Exception as e:
                        print(f"[WARN] Failed to initialize OpenAI: {e}")

            if selected_provider == "gemini":
                add_gemini()
            elif selected_provider == "openai":
                add_openai()
            else:
                # Default / Auto: Try Gemini first, then OpenAI
                add_gemini()
                add_openai()
        
        if not self.providers:
             print("[WARN] No LLM providers initialized. Check API keys and LLM_PROVIDER setting.")

    def generate_content(self, prompt: str, image: Image.Image) -> str:
        if not self.providers:
            raise RuntimeError("No LLM providers configured or available (check API keys).")

        errors = []
        for i, provider in enumerate(self.providers):
            try:
                result = provider.generate_content(prompt, image)
                return result
            except Exception as e:
                error_msg = str(e).lower()
                errors.append(f"{type(provider).__name__}: {str(e)}")
                
                is_last_provider = (i == len(self.providers) - 1)
                
                limit_keywords = ["limit", "quota", "429", "exhausted", "resource"]
                is_limit_error = any(k in error_msg for k in limit_keywords)
                
                if is_last_provider:
                    # No more providers to try
                    raise RuntimeError(f"All LLM providers failed. Last error: {str(e)}") from e
                
                if is_limit_error:
                    print(f"[WARN] Provider {type(provider).__name__} hit rate limit/quota ({str(e)}). Failing over...")
                else:
                    print(f"[WARN] Provider {type(provider).__name__} failed ({str(e)}). Failing over...")
                
                continue
        
        raise RuntimeError(f"All LLM providers failed: {'; '.join(errors)}")

    def generate_text(self, prompt: str) -> str:
        if not self.providers:
            raise RuntimeError("No LLM providers configured or available (check API keys).")

        errors = []
        for i, provider in enumerate(self.providers):
            try:
                result = provider.generate_text(prompt)
                return result
            except Exception as e:
                error_msg = str(e).lower()
                errors.append(f"{type(provider).__name__}: {str(e)}")
                
                is_last_provider = (i == len(self.providers) - 1)
                limit_keywords = ["limit", "quota", "429", "exhausted", "resource"]
                is_limit_error = any(k in error_msg for k in limit_keywords)
                
                if is_last_provider:
                    raise RuntimeError(f"All LLM providers failed. Last error: {str(e)}") from e
                
                if is_limit_error:
                    print(f"[WARN] Provider {type(provider).__name__} hit rate limit/quota ({str(e)}). Failing over...")
                else:
                    print(f"[WARN] Provider {type(provider).__name__} failed ({str(e)}). Failing over...")
                
                continue
        
        raise RuntimeError(f"All LLM providers failed: {'; '.join(errors)}")
