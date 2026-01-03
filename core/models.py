"""MediaPipe FaceLandmarker model loader."""

from mediapipe.tasks.python.vision import FaceLandmarker, FaceLandmarkerOptions
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision.core import vision_task_running_mode


def load_face_landmarker(model_path: str = "face_landmarker.task") -> FaceLandmarker:
    """Load MediaPipe FaceLandmarker from model file."""
    base_options = BaseOptions(model_asset_path=model_path)
    options = FaceLandmarkerOptions(
        base_options=base_options,
        running_mode=vision_task_running_mode.VisionTaskRunningMode.IMAGE,
        num_faces=1,
        output_face_blendshapes=False,
        output_facial_transformation_matrixes=False
    )
    return FaceLandmarker.create_from_options(options)

