import time
import os
import json
import tempfile
from PIL import Image
from google import genai
from dotenv import load_dotenv

load_dotenv()


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
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)

    # Save frame temporarily
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        Image.fromarray(frame).save(tmp.name)
        image = Image.open(tmp.name)

    prompt = get_focused_element_prompt()

    response = client.models.generate_content(
        model=os.getenv("LLM_MODEL"), contents=[prompt, image]
    )

    text = response.text.strip()
    start = text.find("{")
    end = text.rfind("}") + 1

    return json.loads(text[start:end])

def assert_screen_with_llm(frame, expected_content, retries=3, delay=1.0):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)

    for attempt in range(1, retries + 1):
        # Save frame temporarily
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            Image.fromarray(frame).save(tmp.name)
            image = Image.open(tmp.name)

        prompt = get_assertion_prompt(expected_content)

        response = client.models.generate_content(
            model=os.getenv("LLM_MODEL"),
            contents=[prompt, image]
        )

        text = response.text.strip()
        start = text.find("{")
        end = text.rfind("}") + 1

        try:
            result = json.loads(text[start:end])
        except Exception:
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