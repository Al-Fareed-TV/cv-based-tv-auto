import cv2
from camera.realtime_camera import RealTimeCamera

RTSP_URL = "rtsp://192.168.1.99:1945/"

def main():
    cam = RealTimeCamera(RTSP_URL)
    cam.start()

    print("Press 'q' to quit (click on the video window first)")

    while True:
        ret, frame = cam.read()
        if not ret:
            continue

        cv2.imshow("REALTIME RTSP FEED", frame)

        # IMPORTANT: use waitKey(10), not 1
        key = cv2.waitKey(10) & 0xFF
        if key == ord('q'):
            print("Quitting...")
            break

    cam.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
