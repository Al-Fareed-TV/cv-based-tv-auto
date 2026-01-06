import time
import json
import os
import argparse
from datetime import datetime

from camera.realtime_camera import RealTimeCamera
from cv.llm_focus_detector import detect_focus_with_gemini, get_llm_manager
from cv.llm.manager import LLMManager
from dotenv import load_dotenv
from controller.tv_controller import SamsungRemote 
from utils.logger import log_event
from utils.reader import load_text_file

load_dotenv()

# ---------------- CONFIG ---------------- #

RTSP_URL = os.getenv("RTSP_URL")
LLM_INTERVAL_SECONDS = float(os.getenv("LLM_INTERVAL_SECONDS"))
KEY_PRESS_DELAY = float(os.getenv("KEY_PRESS_DELAY"))
POST_ACTION_DELAY = float(os.getenv("POST_ACTION_DELAY"))

# --------------------------------------- #


def decide_next_action(manager, system_prompt, flow_prompt, focus_label):
    prompt = f"""
{system_prompt}

Navigation Goal:
{flow_prompt}

Current focused element:
{focus_label}
"""

    text = manager.generate_text(prompt)

    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
    except Exception as e:
        print(f"[ERROR] JSON parse failed during navigation decision: {e}. Raw Text: {text}")
        # Return a safe fallback or re-raise
        raise

def parse_args():
    parser = argparse.ArgumentParser(
        description="TV automation runner using camera + Multi-LLM Support"
    )
    parser.add_argument(
        "prompt_file",
        help="Path to flow prompt file (e.g. tests/remote_test.txt)"
    )
    parser.add_argument(
        "--provider",
        choices=["auto", "gemini", "openai"],
        default="auto",
        help="LLM Provider to use (auto|gemini|openai). Default: auto (Failover)"
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
    
    # 🌍 Set LLM Provider from CLI arg
    if args.provider:
        os.environ["LLM_PROVIDER"] = args.provider
        print(f"🔹 LLM Provider set to: {args.provider}")

    # Initialize Manager (will read env var)
    # We use get_llm_manager to share the instance with focus detector if possible,
    # or just create a new one. Since get_llm_manager is available, let's use it
    # to ensure consistency if it does caching (currently simple singleton).
    manager = get_llm_manager()

    system_prompt = load_text_file("prompts/system_flow.txt")
    flow_prompt = load_text_file(args.prompt_file)

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
            # This function internally calls get_llm_manager(), so it uses the same config
            focus_result = detect_focus_with_gemini(frame)
            log_event(step_id, "Received focus detection result")

            focused_element = focus_result["focused_element"]
            focus_label = focused_element.get("label")

            print("\n🎯 CURRENT FOCUS:")
            print(focused_element)

            # 3️⃣ Text LLM – navigation decision
            log_event(step_id, "Sending context to Text LLM for navigation decision")
            decision = decide_next_action(
                manager,
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
