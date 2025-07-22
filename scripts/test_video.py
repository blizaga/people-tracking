import cv2
import os

video_path = os.path.join("data", "videos", "test-1.mp4")
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print(f"Failed to open video: {video_path}")
    exit(1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video.")
        break
    cv2.imshow("Video Playback", frame)
    if cv2.waitKey(25) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
