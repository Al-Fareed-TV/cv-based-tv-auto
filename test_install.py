import os
from core.context import DriverContext
from dotenv import load_dotenv


load_dotenv()
RTSP_URL = os.getenv("RTSP_URL")

def test_install():
    ctx = DriverContext(RTSP_URL)
    ctx.start()
    try: 
        ctx.press("HOME")
        ctx.goto("For You", "Search")
        ctx.press("ENTER")
        ctx.goto("Search Screen", "Search Input")
        ctx.press("ENTER")
        ctx.type("Sony LIV")
        ctx.goto("Search Input" ,"Sony LIV App")
        ctx.press("ENTER")
        ctx.goto("Sony LIV App Installation Screen", "Install")
        ctx.press("ENTER")
        
    finally:
        ctx.shutdown()
        
if __name__ == "__main__":
    test_install()