import os
from datetime import datetime
from threading import Lock

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_NAME = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

_lock = Lock()

def log_event(step_id: int, message: str) -> None:
    """
    Logs an event to both console and a timestamped log file.
    """
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    log_line = f"[{timestamp}] [STEP {step_id}] {message}"

    with _lock:
        print(log_line)

        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(log_line + "\n")
