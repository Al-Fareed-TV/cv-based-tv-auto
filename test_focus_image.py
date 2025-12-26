import cv2
import os
from cv.model import detect_focus


IMAGE_PATH = "resources/screens/sameple_frame.jpg"


def main():
    if not os.path.exists(IMAGE_PATH):
        raise FileNotFoundError(f"Image not found: {IMAGE_PATH}")

    # Load image (this simulates a single video frame)
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
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

