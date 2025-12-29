import time
import json
import os
from camera.realtime_camera import RealTimeCamera
from cv.llm_focus_detector import detect_focus_with_gemini
from google import genai
from dotenv import load_dotenv

load_dotenv()

# ---------------- CONFIG ---------------- #

RTSP_URL = "rtsp://192.168.1.37:1945/"   # change if needed
PROMPT_FILE = "tests/remote_test.txt"

LLM_INTERVAL_SECONDS = 2.0   # throttle Gemini calls

# --------------------------------------- #


def load_flow_prompt():
    if not os.path.exists(PROMPT_FILE):
        raise FileNotFoundError(f"{PROMPT_FILE} not found")

    with open(PROMPT_FILE, "r") as f:
        return f.read().strip()


def decide_next_action(client, flow_prompt, focus_label):
    """
    Ask Gemini (TEXT) what the NEXT navigation action should be.
    """

    prompt = f"""
You are controlling navigation in a Smart TV application.

High-level goal:
{flow_prompt}

Current focused element:
{focus_label}

Rules:
- Decide ONLY the NEXT navigation action.
- Valid actions: UP, DOWN, LEFT, RIGHT, ENTER, NONE
- Return exactly ONE action.
- If goal is achieved, return NONE.

Respond ONLY in valid JSON:
{{
  "current_focus": "{focus_label}",
  "next_action": "UP|DOWN|LEFT|RIGHT|ENTER|NONE",
  "confidence": 0.0-1.0
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt]
    )

    text = response.text.strip()
    start = text.find("{")
    end = text.rfind("}") + 1

    return json.loads(text[start:end])


def main():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)

    flow_prompt = load_flow_prompt()
    print("📜 Loaded flow prompt:")
    print(flow_prompt)
    print("-" * 50)

    camera = RealTimeCamera(RTSP_URL)
    camera.start()

    last_llm_call = 0

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                continue

            now = time.time()
            if now - last_llm_call < LLM_INTERVAL_SECONDS:
                continue

            last_llm_call = now

            # 1️⃣ Detect current focus (VISION)
            focus_result = detect_focus_with_gemini(frame)

            focused_element = focus_result["focused_element"]
            focus_label = focused_element.get("label")

            print("\n🎯 CURRENT FOCUS:")
            print(focused_element)

            # 2️⃣ Decide next navigation step (REASONING)
            decision = decide_next_action(
                client,
                flow_prompt,
                focus_label
            )

            print("🧭 NAVIGATION DECISION:")
            print(decision)

            if decision["next_action"] == "NONE":
                print("✅ Flow completed")
                break

            # 🔜 Execution layer goes here
            # Example:
            # samsung_remote.send_key(KEY_MAP[decision["next_action"]])

    finally:
        camera.stop()


if __name__ == "__main__":
    main()
