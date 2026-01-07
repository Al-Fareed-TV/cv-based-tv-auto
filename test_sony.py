import os
from core.context import DriverContext
from dotenv import load_dotenv


load_dotenv()
RTSP_URL = os.getenv("RTSP_URL")

def test_sony():
    ctx = DriverContext(RTSP_URL)
    ctx.start()
    try:
        # Open Sony LIV App 
        ctx.press("HOME")
        ctx.goto("For You", "Sony LIV")
        ctx.press("ENTER")

        # Search CID and Open Video
        ctx.goto("Sony LIV Home", "Sony LIV Search")
        ctx.press("ENTER")
        ctx.type("CID")
        ctx.goto("Sony LIV Search", "Search Banner")
        ctx.press("ENTER")

        # Verify Video is playing
        ctx.press("ENTER")
        ctx.assert_screen("Is this a video player screen")

        # Close the video
        ctx.press("BACK")

        # Close the app
        ctx.press("HOME")
  
    finally:
        ctx.shutdown()
        
if __name__ == "__main__":
    test_sony()