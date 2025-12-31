import time
import os
import argparse
import cv2
from actions.navigator import Navigator
from camera.realtime_camera import RealTimeCamera
from cv.llm_focus_detector import detect_focus_with_gemini
from google import genai
from dotenv import load_dotenv
from utils.logger import log_event
from utils.reader import load_text_file
from controller.tv_controller import SamsungRemote

load_dotenv()
# ---------------- CONFIG ---------------- #

RTSP_URL = os.getenv("RTSP_URL")
LLM_INTERVAL_SECONDS = os.getenv("LLM_INTERVAL_SECONDS")
KEY_PRESS_DELAY = os.getenv("KEY_PRESS_DELAY")  
POST_ACTION_DELAY = os.getenv("POST_ACTION_DELAY") 

# --------------------------------------- #

def parse_args():
    parser = argparse.ArgumentParser(
        description="TV automation runner using camera + Gemini"
    )
    parser.add_argument(
        "prompt_file",
        help="Path to flow prompt file (e.g. tests/remote_test.txt)"
    )
    return parser.parse_args()

def main():
    NAV_MAP_PATH = "config/navigation_map.yaml"
    remote = SamsungRemote();
    nav = Navigator(NAV_MAP_PATH,remote)
    remote.connect();

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)

    system_prompt = load_text_file("prompts/system_flow.txt")

    # camera = RealTimeCamera(RTSP_URL)
    # camera.start()
    
    last_llm_call = 0
    step_id = 0  
    
    try:
        while True:
            # ret, frame = camera.read()
            # if not ret:
            #     continue

            # now = time.time()
            # if now - last_llm_call < LLM_INTERVAL_SECONDS:
            #     continue

            # last_llm_call = now
            IMAGE_PATH = "resources/screens/sample_frame.jpg"
            frame = cv2.imread(IMAGE_PATH)

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
            next_action = nav.goto("For You","Search",0.5)


            # 3️⃣ Check completion
            if next_action == "NONE":
                print("✅ Flow completed by LLM")
                break

            # 5️⃣ Wait for UI to update before next frame
            time.sleep(POST_ACTION_DELAY)

    finally:
        print("ho gya")
        # camera.stop()
        
if __name__ == "__main__":
    main()