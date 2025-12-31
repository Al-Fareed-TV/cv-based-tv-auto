import time
from controller.tv_controller import SamsungRemote
# ^ adjust import if file name differs


def main():
    print("🚀 Starting Samsung Remote Test")

    remote = SamsungRemote()
    remote.connect()

    print("⏳ Waiting for TV authorization...")
    time.sleep(3)

    print("\n🔘 Sending test key sequence")

    # Safe sequence you can visually verify
    test_sequence = [
        "KEY_HOME",   # Go to home screen
        "KEY_RIGHT",  # Move focus right
        "KEY_LEFT",   # Move focus left
        "KEY_UP",     # Move focus up
        "KEY_DOWN",   # Move focus down
        "KEY_BACK" if False else None  # optional
    ]

    for key in test_sequence:
        if key:
            remote.send_key(key)
            time.sleep(1)

    print("\n✅ Test sequence completed")
    print("👀 Verify TV reacted to key presses")

    # Keep process alive briefly to see messages
    time.sleep(5)
    print("🛑 Test finished")


if __name__ == "__main__":
    main()
