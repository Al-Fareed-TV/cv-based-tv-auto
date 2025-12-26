import cv2
import os
from cv.model import detect_focus


IMAGE_PATH = "resources/screens/sample_frame.jpg"


def main():
    if not os.path.exists(IMAGE_PATH):
        raise FileNotFoundError(f"Image not found: {IMAGE_PATH}")

    # Load image (simulates a single video frame)
    frame = cv2.imread(IMAGE_PATH)

    if frame is None:
        raise RuntimeError("Failed to load image")

    bbox = detect_focus(frame)

    if bbox:
        x, y, w, h = bbox
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        print(f"✅ Focus detected at: {bbox}")
    else:
        print("❌ No focus detected")

    cv2.imshow("Focus Detection Result", frame)
    print("Press 'q' or 'ESC' to quit")

    # Wait for quit key
    while True:
        key = cv2.waitKey(50) & 0xFF
        if key == ord('q') or key == 27:  # 27 = ESC
            print("Exiting...")
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
