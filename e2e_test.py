import os
from core.context import DriverContext
from dotenv import load_dotenv
from utils.config import load_json

load_dotenv()
sys_prompt = load_json()
RTSP_URL = os.getenv("RTSP_URL")


def end_to_end_test():
    ctx = DriverContext(RTSP_URL)
    ctx.start()
    try:
        # Open Sony LIV APP
        ctx.press("HOME")
        ctx.longWait()
        ctx.goto("For You","Sony LIV")
        ctx.press("ENTER")
        ctx.longWait(15)
        isSonyLivScreenDisplayed = ctx.assert_screen("Sony LIV Home Screen",sys_prompt["sony_liv_home"])
        print("Is user viewing sony liv screen",isSonyLivScreenDisplayed)
        ctx.longWait(15)
        ctx.press("DOWN")
        ctx.longWait(5)
        ctx.press("LEFT")
        ctx.longWait(5)
        ctx.goto("Sony LIV Home","Movies")
        ctx.longWait(5)
        ctx.press("ENTER")
        ctx.longWait(5)
        isSonyLivScreenDisplayed = ctx.assert_screen("Sony LIV Movies Screen", sys_prompt["sony_liv_movies"])
        print("Is user viewing movies screen",isSonyLivScreenDisplayed)
        ctx.longWait(10)
        ctx.goto("Sony LIV Movies","Movie")
        ctx.longWait(5)
        ctx.press("ENTER")
        ctx.longWait(10)
        ctx.press("ENTER")
        ctx.longWait(10)
        isSonyLivScreenDisplayed = ctx.assert_screen("Sony LIV Video Player", sys_prompt["sony_liv_video_player"])
        print("Is player is shown on screen",isSonyLivScreenDisplayed)
        ctx.press("RIGHT")
        ctx.longWait()
        ctx.press("LEFT")

        #Plan Check
        ctx.press("RETURN")
        ctx.longWait()
        ctx.press("UP")
        ctx.longWait(10)
        ctx.press("ENTER")
        ctx.longWait()
        isSonyLivScreenDisplayed = ctx.assert_screen("Sony LIV Subscription Screen", sys_prompt["sony_liv_subscription"])
        print("Is user viewing subscription screen",isSonyLivScreenDisplayed)

        # Uninstall the Sony LIV App
        ctx.press("HOME")
        ctx.longWait()
        ctx.goto("For You","App Settings")
        ctx.press("ENTER")
        ctx.longWait()
        isExpectedScreenDisplayed = ctx.assert_screen(
            "Settings(DEVELOP MODE)",
            sys_prompt["settings_develop_mode"]
        )
        print("Is user viewing app screen", isExpectedScreenDisplayed)
        ctx.goto("App Settings", "Sony LIV Delete")
        ctx.press("ENTER")
        ctx.press("LEFT")
        ctx.press("ENTER")

        # Install the Sony LIV App
        ctx.press("HOME")
        isUserOnHomeScreen = ctx.assert_screen("For You",sys_prompt["for_you"])
        print("Is user on Home Screen", isUserOnHomeScreen)
        ctx.goto("For You", "Search")
        ctx.press("ENTER")
        ctx.longWait()
        isExpectedScreenDisplayed = ctx.assert_screen("Search screen",sys_prompt["search"])
        print("Is user viewing search screen", isExpectedScreenDisplayed)

        ctx.goto("Search", "Search Input")
        ctx.press("ENTER")
        isExpectedScreenDisplayed = ctx.assert_screen("Virtual Keyboard",sys_prompt["virtual_keyboard"])
        print("Is virtual keyboard visible", isExpectedScreenDisplayed)
        ctx.type("sony")
        ctx.type("key_space", start_char="y", delay=0.3)
        ctx.type("liv", start_char="key_space", delay=0.3)
        ctx.type("key_search", start_char="v", delay=0.3)
        ctx.press("ENTER")
        ctx.press("ENTER")
        ctx.longWait(7)
        ctx.press("ENTER")

    finally:
        ctx.shutdown()


if __name__ == "__main__":
    end_to_end_test()
