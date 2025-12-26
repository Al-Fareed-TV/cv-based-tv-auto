import cv2
import numpy as np


def detect_focus(frame, debug=False):
    """
    Detect focused element based on WHITE BACKGROUND dominance.
    Returns (x, y, w, h) or None
    """

    # 1️⃣ Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 2️⃣ Detect near-white colors (low saturation, high value)
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 40, 255])
    white_mask = cv2.inRange(hsv, lower_white, upper_white)

    # 3️⃣ Morphology to form solid regions
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    white_mask = cv2.morphologyEx(white_mask, cv2.MORPH_CLOSE, kernel)
    white_mask = cv2.morphologyEx(white_mask, cv2.MORPH_OPEN, kernel)

    # 4️⃣ Find contours
    contours, _ = cv2.findContours(
        white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return None

    best_candidate = None
    best_score = 0

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        area = w * h

        # Ignore tiny white areas (icons, text)
        if area < 1500:
            continue

        # Aspect ratio filter (focused tabs are wide, not square)
        aspect_ratio = w / float(h)
        if aspect_ratio < 1.5:
            continue

        # Calculate white pixel density
        roi = white_mask[y:y+h, x:x+w]
        white_ratio = cv2.countNonZero(roi) / float(area)

        # Focused background is mostly white
        if white_ratio > best_score:
            best_score = white_ratio
            best_candidate = (x, y, w, h)

    return best_candidate
