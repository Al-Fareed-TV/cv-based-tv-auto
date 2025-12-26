import cv2
import numpy as np


def detect_focus(frame):
    h, w = frame.shape[:2]
    screen_area = h * w

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 40, 255])
    mask = cv2.inRange(hsv, lower_white, upper_white)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    best = None
    best_confidence = 0.0

    for cnt in contours:
        x, y, bw, bh = cv2.boundingRect(cnt)
        area = bw * bh
        if area < 1500:
            continue

        roi = mask[y:y+bh, x:x+bw]
        white_ratio = cv2.countNonZero(roi) / float(area)

        aspect_ratio = bw / float(bh)
        shape_score = min(1.0, max(0.0, (aspect_ratio - 1.0) / 3.0))

        area_ratio = area / float(screen_area)
        area_score = 1.0 if 0.01 <= area_ratio <= 0.15 else 0.3

        confidence = (
            0.45 * white_ratio +
            0.25 * shape_score +
            0.20 * area_score
        )

        if confidence > best_confidence:
            best_confidence = confidence
            best = (x, y, bw, bh)

    if best is None:
        return None

    return {
        "bbox": best,
        "confidence": round(best_confidence, 2),
        "method": "cv"
    }
