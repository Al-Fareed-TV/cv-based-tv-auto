import time
import json
import tempfile
from PIL import Image
from dotenv import load_dotenv
from cv.llm.manager import LLMManager

load_dotenv()

# Initialize the manager once (or lazily)
_llm_manager = None

def get_llm_manager():
    global _llm_manager
    if _llm_manager is None:
        _llm_manager = LLMManager()
    return _llm_manager


def get_focused_element_prompt():
    return """
You are analyzing a Smart TV application UI.

Exactly ONE UI element is currently focused.
Focused elements have a visually distinct background or emphasis
(such as a white background, highlighted container, or enlargement).

Return ONLY valid JSON:
{
  "focused_element": {
    "label": "<string or null>",
    "bbox": [x, y, width, height],
  }
}
"""

def get_assertion_prompt(expected_content):
    return f"""
You are validating a Smart TV screen.

Task:
Determine whether the CURRENT screen contains the following expected content:

Expected content:
"{expected_content}"

Rules:
- Focus ONLY on the TV UI.
- Ignore reflections, room background, or camera artifacts.
- Answer strictly based on visible UI text, icons, or sections.

Respond ONLY in valid JSON:
{{
  "match": true | false,
  "confidence": 0.0-1.0
}}
"""


def detect_focus_with_gemini(frame):
    """
    Detects the focused element using the configured LLM provider(s).
    Renamed internally to use Manager, but kept function name for compatibility if needed.
    (Though better to rename to detect_focus in future, keeping compat for now).
    """
    manager = get_llm_manager()

    # Convert numpy frame (from opencv) to PIL Image
    image = Image.fromarray(frame)

    prompt = get_focused_element_prompt()

    text = manager.generate_content(prompt, image)

    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
    except Exception as e:
        print(f"[ERROR] JSON parse failed: {e}. Raw Text: {text}")
        raise

def assert_screen_with_llm(frame, expected_content, retries=3, delay=1.0):
    manager = get_llm_manager()

    for attempt in range(1, retries + 1):
        image = Image.fromarray(frame)
        prompt = get_assertion_prompt(expected_content)

        try:
            text = manager.generate_content(prompt, image)
            
            start = text.find("{")
            end = text.rfind("}") + 1
            result = json.loads(text[start:end])
        except Exception as e:
            print(f"[WARN] Assertion attempt {attempt} failed: {e}")
            result = {"match": False, "confidence": 0.0}

        match = result.get("match", False)
        confidence = result.get("confidence", 0.0)

        print(
            f"[ASSERT] Attempt {attempt}/{retries} | "
            f"match={match} confidence={confidence}"
        )

        if match:
            return True

        time.sleep(delay)

    return False
def detect_focus(frame):
    manager = get_llm_manager()

    image = Image.fromarray(frame)
    prompt = get_focused_element_prompt()

    text = manager.generate_content(prompt, image)

    start = text.find("{")
    end = text.rfind("}") + 1
    return json.loads(text[start:end])
