import numpy as np
import cv2

def is_inside_polygon(polygon, point):
    polygon_np = np.array(polygon, np.int32)
    result = cv2.pointPolygonTest(polygon_np, point, False)
    return result >= 0
