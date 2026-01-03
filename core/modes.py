"""Censoring mode definitions."""

from typing import Callable, Dict, Tuple
import cv2
import numpy as np


def apply_blur_to_bbox(img: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
    """Apply Gaussian blur to rectangular region."""
    img_copy = img.copy()
    x1, y1, x2, y2 = bbox
    
    if x2 <= x1 or y2 <= y1:
        return img_copy
    
    width = x2 - x1
    height = y2 - y1
    kernel_size = max(51, min(201, (width + height) // 4))
    kernel_size = kernel_size if kernel_size % 2 == 1 else kernel_size + 1
    sigma = kernel_size / 3.0
    
    region = img_copy[y1:y2, x1:x2]
    if region.size > 0:
        blurred = cv2.GaussianBlur(region, (kernel_size, kernel_size), sigma)
        img_copy[y1:y2, x1:x2] = blurred
    
    return img_copy


def apply_black_to_bbox(img: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
    """Apply solid black fill to rectangular region."""
    img_copy = img.copy()
    x1, y1, x2, y2 = bbox
    
    if x2 <= x1 or y2 <= y1:
        return img_copy
    
    img_copy[y1:y2, x1:x2] = 0
    return img_copy


def apply_pixel_to_bbox(img: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
    """Apply pixelation to rectangular region."""
    img_copy = img.copy()
    x1, y1, x2, y2 = bbox
    
    if x2 <= x1 or y2 <= y1:
        return img_copy
    
    region = img_copy[y1:y2, x1:x2]
    if region.size > 0:
        h_region, w_region = region.shape[:2]
        small = cv2.resize(region, (max(1, w_region // 10), max(1, h_region // 10)), 
                          interpolation=cv2.INTER_LINEAR)
        pixelated = cv2.resize(small, (w_region, h_region), interpolation=cv2.INTER_NEAREST)
        img_copy[y1:y2, x1:x2] = pixelated
    
    return img_copy


def apply_mosaic_to_bbox(img: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
    """Apply mosaic effect to rectangular region."""
    img_copy = img.copy()
    x1, y1, x2, y2 = bbox
    
    if x2 <= x1 or y2 <= y1:
        return img_copy
    
    region = img_copy[y1:y2, x1:x2]
    if region.size > 0:
        h_region, w_region = region.shape[:2]
        small = cv2.resize(region, (max(1, w_region // 8), max(1, h_region // 8)), 
                          interpolation=cv2.INTER_AREA)
        mosaic = cv2.resize(small, (w_region, h_region), interpolation=cv2.INTER_NEAREST)
        img_copy[y1:y2, x1:x2] = mosaic
    
    return img_copy


def apply_white_to_bbox(img: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
    """Apply white fill to rectangular region."""
    img_copy = img.copy()
    x1, y1, x2, y2 = bbox
    
    if x2 <= x1 or y2 <= y1:
        return img_copy
    
    img_copy[y1:y2, x1:x2] = 255
    return img_copy


def apply_noise_to_bbox(img: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
    """Apply noise to rectangular region."""
    img_copy = img.copy()
    x1, y1, x2, y2 = bbox
    
    if x2 <= x1 or y2 <= y1:
        return img_copy
    
    region = img_copy[y1:y2, x1:x2]
    if region.size > 0:
        noise = np.random.randint(0, 256, region.shape, dtype=np.uint8)
        img_copy[y1:y2, x1:x2] = noise
    
    return img_copy


def apply_invert_to_bbox(img: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
    """Apply color inversion to rectangular region."""
    img_copy = img.copy()
    x1, y1, x2, y2 = bbox
    
    if x2 <= x1 or y2 <= y1:
        return img_copy
    
    region = img_copy[y1:y2, x1:x2]
    if region.size > 0:
        inverted = cv2.bitwise_not(region)
        img_copy[y1:y2, x1:x2] = inverted
    
    return img_copy


def apply_strong_blur_to_bbox(img: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
    """Apply very strong Gaussian blur to rectangular region."""
    img_copy = img.copy()
    x1, y1, x2, y2 = bbox
    
    if x2 <= x1 or y2 <= y1:
        return img_copy
    
    region = img_copy[y1:y2, x1:x2]
    if region.size > 0:
        width = x2 - x1
        height = y2 - y1
        kernel_size = max(101, min(301, (width + height) // 2))
        kernel_size = kernel_size if kernel_size % 2 == 1 else kernel_size + 1
        sigma = kernel_size / 2.0
        blurred = cv2.GaussianBlur(region, (kernel_size, kernel_size), sigma)
        img_copy[y1:y2, x1:x2] = blurred
    
    return img_copy


def apply_light_blur_to_bbox(img: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
    """Apply light Gaussian blur to rectangular region."""
    img_copy = img.copy()
    x1, y1, x2, y2 = bbox
    
    if x2 <= x1 or y2 <= y1:
        return img_copy
    
    region = img_copy[y1:y2, x1:x2]
    if region.size > 0:
        blurred = cv2.GaussianBlur(region, (31, 31), 10)
        img_copy[y1:y2, x1:x2] = blurred
    
    return img_copy


AVAILABLE_MODES: Dict[str, Callable] = {
    "blur": apply_blur_to_bbox,
    "black": apply_black_to_bbox,
    "pixel": apply_pixel_to_bbox,
    "mosaic": apply_mosaic_to_bbox,
    "white": apply_white_to_bbox,
    "noise": apply_noise_to_bbox,
    "invert": apply_invert_to_bbox,
    "strong_blur": apply_strong_blur_to_bbox,
    "light_blur": apply_light_blur_to_bbox,
}


def get_available_modes() -> list:
    """Get list of available censoring modes."""
    return list(AVAILABLE_MODES.keys())

