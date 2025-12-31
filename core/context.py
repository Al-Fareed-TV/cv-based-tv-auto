import time
from camera.realtime_camera import RealTimeCamera
from controller.tv_controller import SamsungRemote
from actions.navigator import Navigator
from cv.llm_focus_detector import detect_focus_with_gemini
from utils.logger import log_event


class AutomationContext:
    def __init__(
        self,
        rtsp_url,
        nav_map_path,
        camera_enabled=True
    ):
        self.step = 0

        self.remote = SamsungRemote()
        self.navigator = Navigator(self.remote)

        self.camera = (
            RealTimeCamera(rtsp_url) if camera_enabled else None
        )

    def start(self):
        self.remote.connect()
        if self.camera:
            self.camera.start()

    def shutdown(self):
        if self.camera:
            self.camera.stop()

    def get_focus(self):
        if not self.camera:
            return None

        ret, frame = self.camera.read()
        if not ret:
            return None

        self.step += 1
        log_event(self.step, "Sending frame to LLM for focus detection")

        result = detect_focus_with_gemini(frame)
        return result["focused_element"]["label"]


    def goto(self, destination):
        current_focus = self.get_focus()
        log_event(self.step, f"GOTO from [{current_focus}] to [{destination}]")
        self.navigator.goto(current_focus, destination)

    def press(self, key):
        key_map = {
            "ENTER": "KEY_ENTER",
            "BACK": "KEY_BACK",
            "HOME": "KEY_HOME"
        }

        if key not in key_map:
            raise ValueError(f"Unsupported key action: {key}")

        log_event(self.step, f"PRESS {key}")
        self.remote.send_key(key_map[key])

    def long_press(self, key):
        """
        Long press a remote key for given duration (in seconds).
        """
        log_event(self.step, f"LONG_PRESS {key} ({4}s)")
        self.remote.send_key(f"KEY_{key}")
        time.sleep(4)

    # Placeholder for future
    def type(self, text):
        log_event(self.step, f"TYPE '{text}'")
        raise NotImplementedError("Virtual keyboard typing not implemented yet")
