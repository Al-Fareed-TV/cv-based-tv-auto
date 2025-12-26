from cv.llm_focus_detector import detect_focus_with_gemini

IMAGE_PATH = "resources/screens/sample_frame.jpg"

result = detect_focus_with_gemini(IMAGE_PATH)

print("LLM Focus Result:")
print(result)
