"""MediaPipe Face Landmark definitions and bounding box extraction."""

import numpy as np
from typing import List, Tuple, Any

FACEMESH_LEFT_EYE = [
    33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246
]
FACEMESH_RIGHT_EYE = [
    362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398
]
FACEMESH_LIPS = [
    61, 146, 91, 181, 84, 17, 314, 405, 320, 307, 375, 321, 308, 324, 318, 13,
    82, 81, 80, 78, 95, 88, 178, 87, 14, 317, 402, 318, 324
]


def get_eye_bbox(landmarks: List[Any], img_shape: Tuple[int, int], padding: float = 0.12) -> Tuple[int, int, int, int]:
    """Get bounding box for both eyes combined."""
    h, w = img_shape
    all_eye_points = []
    
    for idx in FACEMESH_LEFT_EYE + FACEMESH_RIGHT_EYE:
        if idx < len(landmarks):
            lm = landmarks[idx]
            all_eye_points.append((lm.x * w, lm.y * h))
    
    if not all_eye_points:
        return (0, 0, 0, 0)
    
    xs = [p[0] for p in all_eye_points]
    ys = [p[1] for p in all_eye_points]
    
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    width = max_x - min_x
    height = max_y - min_y
    
    x1 = int(max(0, center_x - width * (0.5 + padding)))
    y1 = int(max(0, center_y - height * (0.5 + padding)))
    x2 = int(min(w, center_x + width * (0.5 + padding)))
    y2 = int(min(h, center_y + height * (0.5 + padding)))
    
    return (x1, y1, x2, y2)


def get_mouth_bbox(landmarks: List[Any], img_shape: Tuple[int, int], padding: float = 0.12) -> Tuple[int, int, int, int]:
    """Get bounding box for mouth."""
    h, w = img_shape
    mouth_points = []
    
    for idx in FACEMESH_LIPS:
        if idx < len(landmarks):
            lm = landmarks[idx]
            mouth_points.append((lm.x * w, lm.y * h))
    
    if not mouth_points:
        return (0, 0, 0, 0)
    
    xs = [p[0] for p in mouth_points]
    ys = [p[1] for p in mouth_points]
    
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    width = max_x - min_x
    height = max_y - min_y
    
    x1 = int(max(0, center_x - width * (0.5 + padding)))
    y1 = int(max(0, center_y - height * (0.5 + padding)))
    x2 = int(min(w, center_x + width * (0.5 + padding)))
    y2 = int(min(h, center_y + height * (0.5 + padding)))
    
    return (x1, y1, x2, y2)

