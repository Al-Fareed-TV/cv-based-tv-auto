import os
import uuid
import cv2
from datetime import datetime
from threading import Lock

RUN_ID = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
LOG_ROOT = "logs"
RUN_DIR = os.path.join(LOG_ROOT, RUN_ID)
os.makedirs(RUN_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(RUN_DIR, "run.log")

_lock = Lock()


def log_event(step_id: int, message: str) -> None:
    """
    Logs an event to console and run-level log file.
    """
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    log_line = f"[{timestamp}] [STEP {step_id}] {message}"

    with _lock:
        print(log_line)
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")


def save_failed_assertion_frame(frame, screen_name, step_id):
    """
    Saves the failed assertion frame with unique naming.
    """
    ts = datetime.now().strftime("%H-%M-%S")
    uid = uuid.uuid4().hex[:6]

    safe_name = screen_name.replace(" ", "_").replace("/", "_")

    filename = (
        f"ASSERT_FAIL_{safe_name}_"
        f"step_{step_id}_{ts}_{uid}.png"
    )

    path = os.path.join(RUN_DIR, filename)
    cv2.imwrite(path, frame)

    return path
