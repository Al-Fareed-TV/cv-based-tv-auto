import os
import json
import tempfile
from PIL import Image
from google import genai
from dotenv import load_dotenv

load_dotenv()


def detect_focus_with_gemini(frame):
    """
    Takes a numpy frame, sends ONE image to Gemini Vision,
    returns focused element info.
    """

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)

    # Save frame temporarily
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        Image.fromarray(frame).save(tmp.name)
        image = Image.open(tmp.name)

    prompt = """
You are analyzing a Smart TV application UI.

Exactly ONE UI element is currently focused.
Focused elements have a visually distinct background or emphasis
(such as a white background, highlighted container, or enlargement).

Return ONLY valid JSON:
{
  "focused_element": {
    "label": "<string or null>",
    "bbox": [x, y, width, height],
    "confidence": 0.0-1.0
  }
}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=[prompt, image]
    )

    text = response.text.strip()
    start = text.find("{")
    end = text.rfind("}") + 1

    return json.loads(text[start:end])
