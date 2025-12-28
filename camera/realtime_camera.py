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
        # Remove trailing slash if present
        source_url = self.source.rstrip('/') if isinstance(self.source, str) else self.source
        
        print(f"Connecting to RTSP stream: {source_url}")
        
        # Try FFMPEG backend with retries
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Use FFMPEG backend for RTSP
                self.cap = cv2.VideoCapture(source_url, cv2.CAP_FFMPEG)
                
                # Set buffer size to 1 for low latency
                self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                
                # Set additional RTSP options to reduce timeout
                # These options help with connection stability
                self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'H264'))
                
                # Give it a moment to connect
                time.sleep(0.5)
                
                # Try to read a frame to verify connection
                if self.cap.isOpened():
                    ret, test_frame = self.cap.read()
                    if ret:
                        print(f"Successfully connected to RTSP stream (attempt {attempt + 1})")
                        break
                    else:
                        print(f"Connection opened but no frame received (attempt {attempt + 1})")
                        if attempt < max_retries - 1:
                            self.cap.release()
                            time.sleep(1)  # Wait before retry
                            continue
                else:
                    print(f"Failed to open stream (attempt {attempt + 1})")
                    if attempt < max_retries - 1:
                        time.sleep(1)  # Wait before retry
                        continue
            except Exception as e:
                print(f"Error during connection attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
        
        if not self.cap or not self.cap.isOpened():
            raise RuntimeError(
                f"Unable to open RTSP stream after {max_retries} attempts: {source_url}\n"
                "Please check:\n"
                "1. The RTSP server is running and accessible\n"
                "2. Network connectivity to the RTSP server\n"
                "3. The RTSP URL is correct\n"
                "4. Firewall settings allow RTSP connections"
            )

        self.running = True
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()

        print("Camera started")

    def _update(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.01)
                continue

            with self.lock:
                self.frame = frame

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
        print("Camera stopped")
