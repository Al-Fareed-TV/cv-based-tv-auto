import time
from actions.virtual_keyboard import generate_actions_for_input
from camera.realtime_camera import RealTimeCamera
from controller.tv_controller import SamsungRemote
from actions.navigator import Navigator

from cv.llm_focus_detector import assert_screen_with_llm, detect_focus

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

    def shortWait(self,delay=2):
        time.sleep(delay)

    def longWait(self,delay=5):
        time.sleep(delay)

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
        self.shortWait()
        frame = self.get_frame()

        self.step += 1
        log_event(self.step, "Sending frame to LLM for focus detection")

        result = detect_focus(frame)
        return result["focused_element"]["label"]

    def assert_screen(
        self,
        expected: str,
        retries=3,
        delay=2.5,
        min_confidence=0.6,
    ) -> bool:
        for attempt in range(1, retries + 1):
            frame = self.get_frame()

            self.step += 1
            log_event(self.step, f"ASSERT [{expected}] (attempt {attempt}/{retries})")

            try:
                result = assert_screen_with_llm(
                    frame,
                    expected,
                    retries=1,
                    delay=2.5,
                )
            except Exception as e:
                log_event(self.step, f"LLM assertion error: {e}")
                result = False

            if result:
                log_event(self.step, "ASSERT PASSED")
                return True

            log_event(self.step, "ASSERT FAILED — retrying")
            time.sleep(delay)

        log_event(self.step, f"ASSERT FAILED after {retries} attempts")
        return False

    def goto(self, current_focus, destination):
        log_event(self.step, f"GOTO from [{current_focus}] to [{destination}]")
        self.navigator.goto(current_focus, destination)

    def press(self, key):
        log_event(self.step, f"PRESS {key}")
        self.shortWait()
        self.remote.send_key(f"KEY_{key}")

    def long_press(self, key, duration=3, interval=0.0):
        log_event(self.step, f"LONG_PRESS {key} ({duration}s)")

        end_time = time.time() + duration
        remote_key = f"KEY_{key}"

        while time.time() < end_time:
            self.remote.send_key(remote_key)
            time.sleep(interval)

    def type(self, text, start_char="a", delay=0.5):
        log_event(self.step, f"TYPE '{text}'")

        actions = generate_actions_for_input(text, start_char)

        for key in actions:
            self.remote.send_key(key)
        time.sleep(delay)
