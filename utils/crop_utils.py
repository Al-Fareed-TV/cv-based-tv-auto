"""
Crop Utilities Module

Utility functions for cropping and processing video frames.
Used to focus on specific regions of the TV screen.
"""

import cv2
import numpy as np
from typing import Tuple, Optional


def crop_frame(frame: np.ndarray, x: int, y: int, width: int, height: int) -> np.ndarray:
    """
    Crop a frame to the specified region.
    
    Args:
        frame: Input frame as numpy array
        x: X coordinate of top-left corner
        y: Y coordinate of top-left corner
        width: Width of crop region
        height: Height of crop region
        
    Returns:
        Cropped frame
    """
    if frame is None:
        return np.array([])
    
    h, w = frame.shape[:2]
    
    # Ensure coordinates are within frame bounds
    x = max(0, min(x, w))
    y = max(0, min(y, h))
    width = min(width, w - x)
    height = min(height, h - y)
    
    return frame[y:y+height, x:x+width]


def crop_center(frame: np.ndarray, width: int, height: int) -> np.ndarray:
    """
    Crop the center region of a frame.
    
    Args:
        frame: Input frame
        width: Desired width of center crop
        height: Desired height of center crop
        
    Returns:
        Center-cropped frame
    """
    if frame is None:
        return np.array([])
    
    h, w = frame.shape[:2]
    center_x = w // 2
    center_y = h // 2
    
    x = center_x - width // 2
    y = center_y - height // 2
    
    return crop_frame(frame, x, y, width, height)


def crop_region_percentage(
    frame: np.ndarray,
    x_percent: float,
    y_percent: float,
    width_percent: float,
    height_percent: float
) -> np.ndarray:
    """
    Crop a frame using percentage-based coordinates.
    
    Args:
        frame: Input frame
        x_percent: X position as percentage (0.0 to 1.0)
        y_percent: Y position as percentage (0.0 to 1.0)
        width_percent: Width as percentage (0.0 to 1.0)
        height_percent: Height as percentage (0.0 to 1.0)
        
    Returns:
        Cropped frame
    """
    if frame is None:
        return np.array([])
    
    h, w = frame.shape[:2]
    
    x = int(w * x_percent)
    y = int(h * y_percent)
    width = int(w * width_percent)
    height = int(h * height_percent)
    
    return crop_frame(frame, x, y, width, height)


def resize_frame(frame: np.ndarray, width: Optional[int] = None, height: Optional[int] = None) -> np.ndarray:
    """
    Resize a frame while maintaining aspect ratio if only one dimension is specified.
    
    Args:
        frame: Input frame
        width: Target width (None to maintain aspect ratio)
        height: Target height (None to maintain aspect ratio)
        
    Returns:
        Resized frame
    """
    if frame is None:
        return np.array([])
    
    if width is None and height is None:
        return frame
    
    h, w = frame.shape[:2]
    
    if width is None:
        # Calculate width based on height
        aspect_ratio = w / h
        width = int(height * aspect_ratio)
    elif height is None:
        # Calculate height based on width
        aspect_ratio = h / w
        height = int(width * aspect_ratio)
    
    return cv2.resize(frame, (width, height), interpolation=cv2.INTER_AREA)


def extract_roi(frame: np.ndarray, roi: Tuple[int, int, int, int]) -> np.ndarray:
    """
    Extract a region of interest (ROI) from a frame.
    
    Args:
        frame: Input frame
        roi: Tuple of (x, y, width, height)
        
    Returns:
        Extracted ROI
    """
    x, y, w, h = roi
    return crop_frame(frame, x, y, w, h)

