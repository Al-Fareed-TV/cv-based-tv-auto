import time
from camera.realtime_camera import RealTimeCamera
from controller.tv_controller import SamsungRemote
from actions.navigator import Navigator
from cv.llm_focus_detector import assert_screen_with_llm, detect_focus_with_gemini
from utils.logger import log_event
class DriverContext:
    def __init__(self, rtsp_url, camera_enabled=True):
        self.step = 0

        self.remote = SamsungRemote()
        self.navigator = Navigator(self.remote)

        self.camera = RealTimeCamera(rtsp_url) if camera_enabled else None

    def start(self):
        self.remote.connect()
        if self.camera:
            self.camera.start()

    def shutdown(self):
        if self.camera:
            self.camera.stop()

    def get_frame(self, timeout=5.0):
        if not self.camera:
            raise RuntimeError("Camera is disabled")

        start_time = time.time()

        while True:
            ret, frame = self.camera.read()
            if ret and frame is not None:
                return frame

            if time.time() - start_time > timeout:
                raise RuntimeError("Timeout waiting for camera frame")

            time.sleep(0.05)

    def get_focus(self):
        frame = self.get_frame()

        self.step += 1
        log_event(self.step, "Sending frame to LLM for focus detection")

        result = detect_focus_with_gemini(frame)
        return result["focused_element"]["label"]

    def assert_screen(self, expected, retries=3, delay=1.0):
        for attempt in range(1, retries + 1):
            frame = self.get_frame()

            self.step += 1
            log_event(
                self.step,
                f"Asserting screen [{expected}] (attempt {attempt}/{retries})",
            )

            if assert_screen_with_llm(frame, expected):
                return True

            time.sleep(delay)

        return False

    def goto(self, destination):
        current_focus = self.get_focus()
        log_event(self.step, f"GOTO from [{current_focus}] to [{destination}]")
        self.navigator.goto(current_focus, destination)

    def press(self, key):
        log_event(self.step, f"PRESS {key}")
        self.remote.send_key(f"KEY_{key}")

    def long_press(self, key, duration=3, interval=0.0):
        log_event(self.step, f"LONG_PRESS {key} ({duration}s)")

        end_time = time.time() + duration
        remote_key = f"KEY_{key}"

        while time.time() < end_time:
            self.remote.send_key(remote_key)
            time.sleep(interval)


    def type(self, text):
        log_event(self.step, f"TYPE '{text}'")
        raise NotImplementedError("Virtual keyboard typing not implemented yet")