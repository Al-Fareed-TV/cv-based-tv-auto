import cv2
import threading
import time


class RealTimeCamera:
    """
    Hard real-time camera reader.
    Always keeps ONLY the latest frame.
    """

    def __init__(self, source):
        self.source = source
        self.cap = None
        self.frame = None
        self.running = False
        self.lock = threading.Lock()
        self.thread = None

    def start(self):
        self.cap = cv2.VideoCapture(self.source, cv2.CAP_FFMPEG)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not self.cap.isOpened():
            raise RuntimeError("❌ Unable to open RTSP stream")

        self.running = True
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()

        print("✅ Real-time camera started")

    def _update(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.01)
                continue

            with self.lock:
                self.frame = frame  # overwrite old frame

    def read(self):
        with self.lock:
            if self.frame is None:
                return False, None
            return True, self.frame.copy()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        if self.cap:
            self.cap.release()
        print("🛑 Camera stopped")
