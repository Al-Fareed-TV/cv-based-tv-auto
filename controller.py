import time
import json
import os
from camera.realtime_camera import RealTimeCamera
from cv.llm_focus_detector import detect_focus_with_gemini
from google import genai


class TVController:
    """
    Orchestrates:
    Camera → Focus Detection → Navigation Decision → Execution
    """

    def __init__(self, camera_source, flow_prompt):
        self.camera = RealTimeCamera(camera_source)
        self.flow_prompt = flow_prompt
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        self.last_llm_call = 0
        self.llm_interval = 2.0  # seconds

    def start(self):
        self.camera.start()

        try:
            while True:
                ret, frame = self.camera.read()
                if not ret:
                    continue

                now = time.time()
                if now - self.last_llm_call < self.llm_interval:
                    continue

                self.last_llm_call = now

                # 1️⃣ Detect focus via Gemini Vision
                focus = detect_focus_with_gemini(frame)
                current_focus = focus["focused_element"]["label"]

                print("FOCUS:", current_focus)

                # 2️⃣ Decide next navigation
                decision = self._decide_navigation(current_focus)
                print("DECISION:", decision)

                # 3️⃣ Execute navigation
                self._execute(decision["next_action"])

                if decision["next_action"] == "NONE":
                    print("Flow completed")
                    break

        finally:
            self.camera.stop()

    def _decide_navigation(self, current_focus):
        prompt = f"""
You are navigating a Smart TV UI.

Goal:
{self.flow_prompt}

Current focused element:
{current_focus}

Decide the NEXT navigation step.

Rules:
- Valid actions: UP, DOWN, LEFT, RIGHT, ENTER, NONE
- Return ONLY ONE action
- Stop when goal is achieved

Respond ONLY in JSON:
{{
  "current_focus": "{current_focus}",
  "next_action": "UP|DOWN|LEFT|RIGHT|ENTER|NONE",
  "confidence": 0.0-1.0
}}
"""

        response = self.client.models.generate_content(
            model="gemini-1.0-pro",
            contents=[prompt]
        )

        text = response.text.strip()
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])

    def _execute(self, action):
        if action == "NONE":
            return

        # Stub: replace with IR / HDMI-CEC / ADB
        print(f"EXECUTE: {action}")
        time.sleep(0.8)
