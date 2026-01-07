import time
import os
from core.context import DriverContext
from dotenv import load_dotenv

load_dotenv()

RTSP_URL = os.getenv("RTSP_URL")

def end_to_end_test():
    ctx = DriverContext(RTSP_URL)
    ctx.start()
    try:
        ctx.goto("For You","App Settings")
        ctx.press("ENTER")
        ctx.longWait()
        isExpectedScreenDisplayed =  ctx.assert_screen("Am I in Settings(DEVELOPE MODE) page?")
        print("Is user viewing app screen",isExpectedScreenDisplayed)
        ctx.goto("App Settings","Sony LIV Delete")
        ctx.press("ENTER")
        ctx.press("LEFT")
        ctx.press("ENTER")

        ctx.press("HOME")
        isUserOnHomeScreen = ctx.assert_screen("Am I in ```For You``` tab?")
        print("Is user on Home Screen",isUserOnHomeScreen)
        ctx.goto("For You","Search")
        ctx.press("ENTER")
        ctx.longWait()
        isExpectedScreenDisplayed = ctx.assert_screen("Am I in Search screen?")
        print("Is user viewing search screen",isExpectedScreenDisplayed)

        ctx.goto("Search","Search Input")
        ctx.press("ENTER")
        isExpectedScreenDisplayed =  ctx.assert_screen("Is Virtual Keyboard Visible?")
        print("Is virtual keyboard visible",isExpectedScreenDisplayed)
        ctx.type("sony")
        ctx.type("key_space",start_char="y",delay=0.3)
        ctx.type("liv",start_char="key_space",delay=0.3)
        ctx.type("key_search",start_char="v",delay=0.3)
        ctx.press("ENTER")
        ctx.press("ENTER")
        ctx.longWait(7)
        ctx.press("ENTER")
       
    finally:
        ctx.shutdown()
        
if __name__ == "__main__":
    end_to_end_test()