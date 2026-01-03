"""Face censoring: eyes and mouth only using rectangles."""

import numpy as np
from typing import List, Tuple, Any
from core.landmarks import get_eye_bbox, get_mouth_bbox
from core.modes import AVAILABLE_MODES


def censor_face(img: np.ndarray, landmarks: List[Any], mode: str = "blur") -> np.ndarray:
    """Apply censoring to eyes and mouth only using rectangles.
    
    Args:
        img: BGR image
        landmarks: List of NormalizedLandmark objects
        mode: One of: blur, black, pixel, mosaic, white, noise, invert, 
              strong_blur, light_blur (default: blur)
        
    Returns:
        Censored image
    """
    img_copy = img.copy()
    h, w = img.shape[:2]
    
    eye_bbox = get_eye_bbox(landmarks, (h, w))
    mouth_bbox = get_mouth_bbox(landmarks, (h, w))
    
    censor_func = AVAILABLE_MODES.get(mode.lower(), AVAILABLE_MODES["blur"])
    
    if eye_bbox[2] > eye_bbox[0] and eye_bbox[3] > eye_bbox[1]:
        img_copy = censor_func(img_copy, eye_bbox)
    if mouth_bbox[2] > mouth_bbox[0] and mouth_bbox[3] > mouth_bbox[1]:
        img_copy = censor_func(img_copy, mouth_bbox)
    
    return img_copy
