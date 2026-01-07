import os
from core.context import DriverContext
from dotenv import load_dotenv
import time


load_dotenv()
# ---------------- CONFIG ---------------- #

RTSP_URL = os.getenv("RTSP_URL")

def test_search():
    ctx = DriverContext(RTSP_URL)
    ctx.start()
    try:
        ctx.press("Home")
        ctx.goto("For You","App Settings")
        ctx.press("ENTER")
        time.sleep(5)
        isExpectedScreenDisplayed =  ctx.assert_screen("Am I in Settings(DEVELOPE MODE) page?")
        print("Is user viewing app screen",isExpectedScreenDisplayed)
        ctx.goto("App Settings","Sony LIV Delete")
        ctx.press("ENTER")
    finally:
        ctx.shutdown()
        
if __name__ == "__main__":
    test_search()