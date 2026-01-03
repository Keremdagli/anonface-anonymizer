"""Main anonymization module using MediaPipe Face Landmarker."""

import cv2
import numpy as np
from typing import Optional, List, Any
from mediapipe import Image as MpImage, ImageFormat
from mediapipe.tasks.python.vision import FaceLandmarker, FaceLandmarkerOptions
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision.core import vision_task_running_mode
from core.censor import censor_face


class FaceAnonymizer:
    """Face anonymizer using MediaPipe Tasks API."""
    
    def __init__(self, model_path: str = "face_landmarker.task"):
        """Initialize face landmarker."""
        base_options = BaseOptions(model_asset_path=model_path)
        options = FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=vision_task_running_mode.VisionTaskRunningMode.IMAGE,
            num_faces=1,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=False
        )
        self.landmarker = FaceLandmarker.create_from_options(options)
    
    def detect_landmarks(self, img: np.ndarray) -> Optional[List[Any]]:
        """Detect face landmarks in BGR image.
        
        Args:
            img: OpenCV BGR image (numpy array)
            
        Returns:
            List of NormalizedLandmark objects or None if no face detected
        """
        h, w = img.shape[:2]
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = MpImage(image_format=ImageFormat.SRGB, data=rgb)
        results = self.landmarker.detect(mp_image)
        
        if not results.face_landmarks or len(results.face_landmarks) == 0:
            return None
        
        return results.face_landmarks[0]
    
    def anonymize(self, img: np.ndarray, mode: str = "blur") -> Optional[np.ndarray]:
        """Anonymize face in image (eyes and mouth only).
        
        Args:
            img: BGR image
            mode: Censoring mode (default: blur)
            
        Returns:
            Anonymized image or None if no face detected
        """
        landmarks = self.detect_landmarks(img)
        if landmarks is None:
            return None
        
        return censor_face(img, landmarks, mode)

