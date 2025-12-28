import cv2
from cv.llm_focus_detector import detect_focus_with_gemini

frame = cv2.imread("resources/screens/sample_frame.jpg")
result = detect_focus_with_gemini(frame)
print(result)
