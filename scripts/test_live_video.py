import cv2
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.utils.video_source import get_video_capture

cap = get_video_capture()

while True:
    ret, frame = cap.read()
    if not ret:
        print("End of stream/video.")
        break
    cv2.imshow("Video", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
