import os
from core.context import DriverContext
from dotenv import load_dotenv


load_dotenv()
# ---------------- CONFIG ---------------- #

RTSP_URL = os.getenv("RTSP_URL")

def test_search():
    ctx = DriverContext(RTSP_URL)
    ctx.start()
    try: 
        ctx.goto("Sony LIV")
        ctx.long_press("ENTER")
        # isAppsSceenDisplayed =  ctx.assert_screen("Am I in Apps tab?")
        # print("Is user viewing app screen",isAppsSceenDisplayed)
    finally:
        ctx.shutdown()
        
if __name__ == "__main__":
    test_search()