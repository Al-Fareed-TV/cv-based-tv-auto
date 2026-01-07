import unittest
from unittest.mock import MagicMock, patch
from cv.llm.manager import LLMManager
from cv.llm.base import LLMProvider

class TestLLMManager(unittest.TestCase):
    def test_failover_logic(self):
        # Mock providers
        p1 = MagicMock(spec=LLMProvider)
        p1.generate_content.side_effect = RuntimeError("Quota exceeded 429")
        
        p2 = MagicMock(spec=LLMProvider)
        p2.generate_content.return_value = "success"
        
        # Test default auto mode behavior (Gemini -> OpenAI)
        # We manually construct manager with mocked providers to test logic directly
        manager = LLMManager(providers=[p1, p2])
        
        result = manager.generate_content("prompt", MagicMock())
        
        self.assertEqual(result, "success")
        p1.generate_content.assert_called_once()
        p2.generate_content.assert_called_once()

    @patch("cv.llm.manager.GeminiProvider")
    @patch.dict("os.environ", {"LLM_PROVIDER": "gemini", "GEMINI_API_KEY": "test"})
    def test_explicit_selection(self, mock_gemini):
        manager = LLMManager()
        self.assertEqual(len(manager.providers), 1)
        
if __name__ == '__main__':
    unittest.main()
