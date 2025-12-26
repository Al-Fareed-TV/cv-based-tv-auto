import cv2
import numpy as np


def detect_focus(frame):
    """
    Detect focused / highlighted UI element from a single frame.

    Returns:
        (x, y, w, h) or None
    """

    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Highlight detection (bright, low saturation)
    lower = np.array([0, 0, 180])
    upper = np.array([180, 80, 255])
    mask = cv2.inRange(hsv, lower, upper)

    # Morphological cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Find contours
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return None

    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h

        # Ignore small noise
        if area < 2000:
            continue

        return (x, y, w, h)

    return None
