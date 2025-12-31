from datetime import datetime

def log_event(step_id: int, message: str) -> None:
    ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"[{ts}] [STEP {step_id}] {message}")