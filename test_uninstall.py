import os
from core.context import DriverContext
from dotenv import load_dotenv


load_dotenv()
RTSP_URL = os.getenv("RTSP_URL")

def test_uninstall():
    ctx = DriverContext(RTSP_URL)
    ctx.start()
    try: 
        ctx.goto("App Settings")
        ctx.press("ENTER")
        ctx.goto("Sony LIV Delete")
        ctx.press("ENTER")
        ctx.goto("Delete")
        ctx.press("ENTER")
    finally:
        ctx.shutdown()
        
if __name__ == "__main__":
    test_uninstall()