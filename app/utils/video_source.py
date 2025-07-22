from app.core.config import settings
import cv2


def get_video_capture(source_type=None, source_path=None):
    """
    source_type: 'live' or 'static'
    source_path: URL or file path
    """
    if source_type is None:
        source_type = settings.video_source_type
    if source_path is None:
        source_path = settings.video_source_path

    if source_type not in ["live", "static"]:
        raise ValueError(f"Invalid source_type: {source_type}")

    cap = cv2.VideoCapture(source_path)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video source: {source_path}")
    
    print(f"✅ Opened {source_type} video source: {source_path}")
    return cap
