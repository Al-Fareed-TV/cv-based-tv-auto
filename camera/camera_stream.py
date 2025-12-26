import cv2
import time


class CameraStream:
    def __init__(self, source, target_fps=6):
        self.source = source
        self.target_fps = target_fps
        self.cap = None
        self.last_time = 0

    def open(self):
        self.cap = cv2.VideoCapture(self.source, cv2.CAP_FFMPEG)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not self.cap.isOpened():
            raise RuntimeError("Unable to open RTSP stream")

        print("✅ RTSP stream opened (low-latency mode)")

    def read(self):
        now = time.time()
        if now - self.last_time < 1 / self.target_fps:
            return False, None

        self.last_time = now

        # Drop buffered frames
        for _ in range(3):
            self.cap.grab()

        ret, frame = self.cap.retrieve()
        return ret, frame

    def release(self):
        if self.cap:
            self.cap.release()
