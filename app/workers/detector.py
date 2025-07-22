from ultralytics import YOLO
import cv2
import numpy as np
import time
from datetime import datetime
from deep_sort_realtime.deepsort_tracker import DeepSort

from app import models
from app.utils.video_source import get_video_capture
from app.core.database import SessionLocal, get_current_polygon
from app.models.detection import Detection
from app.models.counter import Counter
from app.utils.helper import is_inside_polygon


from ultralytics import YOLO
import cv2
import numpy as np
import time
from datetime import datetime
from deep_sort_realtime.deepsort_tracker import DeepSort

from app import models
from app.utils.video_source import get_video_capture
from app.core.database import SessionLocal
from app.models.detection import Detection
from app.models.counter import Counter
from app.utils.helper import is_inside_polygon
from app.services.area_service import area_service


def run_detection(area_id: str = None):
    """
    Run people detection and tracking
    
    Args:
        area_id: Specific area ID to use. If None, will use default/active area
    """
    session = SessionLocal()
    cap = get_video_capture()

    model = YOLO("yolo11n.pt")
    tracker = DeepSort(max_age=30, n_init=3, max_cosine_distance=0.2, nn_budget=100)

    # Get detection areas dynamically
    detection_areas = area_service.get_detection_areas(session, area_id)
    
    if not detection_areas:
        raise ValueError("No areas configured for detection. Please create an area first.")
    
    print(f"✅ Detection areas loaded: {len(detection_areas)}")
    for area in detection_areas:
        print(f"   - Area: {area.name} ({area.id})")

    # Use first area as primary (for single area mode)
    primary_area = detection_areas[0]
    area_id = str(primary_area.id)
    polygon_area = primary_area.polygon_coordinates
    
    if not polygon_area:
        raise ValueError(f"No polygon configured for area {area_id}")

    print(f"✅ Primary area polygon: {polygon_area}")

    seen_tracks = set()
    last_refresh = time.time()
    REFRESH_INTERVAL = 10  # seconds

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of stream.")
            break

        frame = cv2.resize(frame, (1280, 720))

        # Refresh areas and polygon setiap REFRESH_INTERVAL seconds
        if time.time() - last_refresh > REFRESH_INTERVAL:
            updated_areas = area_service.get_detection_areas(session, area_id)
            if updated_areas:
                updated_area = updated_areas[0]
                updated_polygon = updated_area.polygon_coordinates
                if updated_polygon != polygon_area:
                    print(f"🔷 Polygon updated: {updated_polygon}")
                    polygon_area = updated_polygon
            last_refresh = time.time()

        results = model(frame, verbose=False)[0]

        detections = []
        for box in results.boxes:
            if int(box.cls[0]) == 0:  # person
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                detections.append(([x1, y1, x2 - x1, y2 - y1], conf, "person"))

        tracks = tracker.update_tracks(detections, frame=frame)

        for track in tracks:
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            l, t, r, b = track.to_ltrb()
            cx = int((l + r) / 2)
            cy = int((t + b) / 2)
            bbox = {"x": int(l), "y": int(t), "w": int(r - l), "h": int(b - t)}

            inside = is_inside_polygon(polygon_area, (cx, cy))
            track_key = f"{area_id}:{track_id}"

            if inside:
                if track_key not in seen_tracks:
                    seen_tracks.add(track_key)

                    counter = session.query(Counter).filter_by(area_id=area_id).first()
                    if not counter:
                        counter = Counter(area_id=area_id, in_count=1, updated_at=datetime.utcnow())
                        session.add(counter)
                    else:
                        counter.in_count += 1
                        counter.updated_at = datetime.utcnow()

                det = Detection(
                    tracking_id=str(track_id),
                    area_id=area_id,
                    frame_time=datetime.utcnow(),
                    bbox=bbox,
                    entered=True,
                )
                session.add(det)

                cv2.rectangle(frame, (int(l), int(t)), (int(r), int(b)), (0, 255, 0), 2)
                cv2.putText(frame, f"ID:{track_id}", (int(l), int(t) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)

        session.commit()

        # Draw polygon dan info
        if polygon_area:
            cv2.polylines(frame, [np.array(polygon_area, np.int32)], isClosed=True, color=(255, 0, 0), thickness=2)
        
        # Display area info
        cv2.putText(frame, f"Area: {primary_area.name}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow("People Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    session.close()
