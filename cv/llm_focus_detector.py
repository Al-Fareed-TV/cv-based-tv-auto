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


def get_assertion_prompt(screen_name: str, screen_spec: dict) -> str:
    return f"""
You are a STRICT screen validator for a Smart TV UI.

You are shown ONE image of the TV screen.

Your task:
Verify whether the image MATCHES the expected screen described below.

Screen name:
{screen_name}

Expected screen specification (ground truth):
{json.dumps(screen_spec, indent=2)}

Rules (MANDATORY):
- Use ONLY what is VISIBLE on the TV UI.
- Ignore reflections, room objects, glare, and camera artifacts.
- DO NOT assume or guess missing elements.
- If 50% of required visible element is missing → match = false.
- If 10% or 1 or 2 required visible element is missing → match = True.
- If the screen is ambiguous or unclear → match = false.
- NEVER infer navigation state.
- NEVER explain your reasoning.

Response format (STRICT JSON ONLY):
{{
  "match": true | false,
  "confidence": number   // 0.0 to 1.0
}}

IMPORTANT:
- Output MUST be valid JSON.
- Do NOT include any text outside JSON.
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


def assert_screen_with_llm(
    frame,
    screen_name: str,
    screen_spec: dict,
    retries: int = 3,
    delay: float = 1.0,
    min_confidence: float = 0.6,
) -> bool:
    manager = get_llm_manager()

    for attempt in range(1, retries + 1):
        image = Image.fromarray(frame)
        prompt = get_assertion_prompt(screen_name, screen_spec)

        try:
            text = manager.generate_content(prompt, image)

            start = text.find("{")
            end = text.rfind("}") + 1
            result = json.loads(text[start:end])

            match = bool(result.get("match", False))
            confidence = float(result.get("confidence", 0.0))

        except Exception as e:
            print(f"[WARN] Assertion attempt {attempt} failed: {e}")
            match = False
            confidence = 0.0

        print(
            f"[ASSERT] {screen_name} | "
            f"attempt {attempt}/{retries} | "
            f"match={match} confidence={confidence}"
        )

        if match and confidence >= min_confidence:
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
