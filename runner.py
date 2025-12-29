import time
import json
import os
import argparse
from datetime import datetime

from camera.realtime_camera import RealTimeCamera
from cv.llm_focus_detector import detect_focus_with_gemini
from google import genai
from dotenv import load_dotenv
from controller.tv_controller import SamsungRemote  # ✅ NEW

load_dotenv()

# ---------------- CONFIG ---------------- #

RTSP_URL = "rtsp://192.168.1.37:1945/"
SYSTEM_PROMPT_FILE = "prompts/system_flow.txt"

LLM_INTERVAL_SECONDS = 2.0
KEY_PRESS_DELAY = 0.4          # delay between keys
POST_ACTION_DELAY = 1.2        # wait for UI to settle

# --------------------------------------- #


def log_event(step_id: int, message: str) -> None:
    """
    Structured console logging for LLM decision boundaries.
    Logs only when a frame is selected for LLM processing.
    """
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{ts}] [STEP {step_id}] {message}")


def load_text_file(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r") as f:
        return f.read().strip()


def decide_next_action(client, system_prompt, flow_prompt, focus_label):
    prompt = f"""
{system_prompt}

Navigation Goal:
{flow_prompt}

Current focused element:
{focus_label}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt]
    )

    text = response.text.strip()
    start = text.find("{")
    end = text.rfind("}") + 1

    return json.loads(text[start:end])


def parse_args():
    parser = argparse.ArgumentParser(
        description="TV automation runner using camera + Gemini"
    )
    parser.add_argument(
        "prompt_file",
        help="Path to flow prompt file (e.g. tests/remote_test.txt)"
    )
    return parser.parse_args()


def execute_actions(remote, actions):
    """
    Execute a list of remote key actions sequentially.
    """
    for key in actions:
        print(f"🎮 EXECUTING: {key}")
        remote.send_key(key)
        time.sleep(KEY_PRESS_DELAY)


def main():
    args = parse_args()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)

    system_prompt = load_text_file(SYSTEM_PROMPT_FILE)
    flow_prompt = load_text_file(args.prompt_file)

    print("📜 Loaded system prompt")
    print("📜 Loaded flow prompt")
    print("-" * 50)

    camera = RealTimeCamera(RTSP_URL)
    camera.start()

    # ✅ Initialize Samsung Remote
    remote = SamsungRemote()
    remote.connect()

    last_llm_call = 0
    step_id = 0  # monotonically increasing step counter for LLM decision cycles

    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                continue

            now = time.time()
            if now - last_llm_call < LLM_INTERVAL_SECONDS:
                continue

            last_llm_call = now

            # 1️⃣ Frame selected for LLM processing
            step_id += 1
            log_event(step_id, "Frame selected for LLM processing")

            # 2️⃣ Vision LLM – focus detection
            log_event(step_id, "Sending frame to Vision LLM for focus detection")
            focus_result = detect_focus_with_gemini(frame)
            log_event(step_id, "Received focus detection result")

            focused_element = focus_result["focused_element"]
            focus_label = focused_element.get("label")

            print("\n🎯 CURRENT FOCUS:")
            print(focused_element)

            # 3️⃣ Text LLM – navigation decision
            log_event(step_id, "Sending context to Text LLM for navigation decision")
            decision = decide_next_action(
                client,
                system_prompt,
                flow_prompt,
                focus_label
            )
            log_event(step_id, f"Received navigation decision: {decision['next_action']}")

            print("🧭 LLM DECISION:")
            print(decision)

            next_action = decision["next_action"]

            # 3️⃣ Check completion
            if next_action == "NONE":
                print("✅ Flow completed by LLM")
                break

            # 4️⃣ Execute returned actions
            if isinstance(next_action, list):
                execute_actions(remote, next_action)
            else:
                raise ValueError(
                    f"Invalid next_action format: {next_action}"
                )

            # 5️⃣ Wait for UI to update before next frame
            time.sleep(POST_ACTION_DELAY)

    finally:
        camera.stop()


if __name__ == "__main__":
    main()
