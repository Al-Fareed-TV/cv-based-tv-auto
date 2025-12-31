import os
from core.context import AutomationContext
from dotenv import load_dotenv


load_dotenv()
# ---------------- CONFIG ---------------- #

RTSP_URL = os.getenv("RTSP_URL")

def test_search():
    ctx = AutomationContext(RTSP_URL)
    ctx.start()
    try: 
        ctx.goto("Search")
        ctx.press("ENTER")
    finally:
        ctx.shutdown()
        
if __name__ == "__main__":
    test_search()