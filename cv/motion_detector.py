"""
Motion Detector Module

Detects motion and playback state in video frames.
Used to determine if content is playing vs static screens.
"""

import cv2
import numpy as np
from typing import Optional, Tuple


class MotionDetector:
    """
    Detects motion in video frames to determine playback state.
    
    This helps distinguish between:
    - Static UI screens (home, menu, search)
    - Active playback (video content)
    - Loading states (transitions)
    """
    
    def __init__(self, threshold: float = 25.0, min_area: int = 500):
        """
        Initialize motion detector.
        
        Args:
            threshold: Threshold for motion detection (lower = more sensitive)
            min_area: Minimum area of motion to consider significant
        """
        self.threshold = threshold
        self.min_area = min_area
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500, varThreshold=50, detectShadows=True
        )
        self.previous_frame: Optional[np.ndarray] = None
    
    def detect_motion(self, frame: np.ndarray) -> Tuple[bool, float, np.ndarray]:
        """
        Detect motion in the given frame.
        
        Args:
            frame: Input frame as numpy array
            
        Returns:
            Tuple of (has_motion: bool, motion_percentage: float, motion_mask: np.ndarray)
        """
        if frame is None:
            return False, 0.0, np.zeros((1, 1), dtype=np.uint8)
        
        # Convert to grayscale if needed
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame
        
        # Apply background subtraction
        fg_mask = self.background_subtractor.apply(gray)
        
        # Remove noise
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Calculate motion area
        motion_area = sum(cv2.contourArea(c) for c in contours if cv2.contourArea(c) > self.min_area)
        total_area = frame.shape[0] * frame.shape[1]
        motion_percentage = (motion_area / total_area) * 100
        
        # Determine if significant motion exists
        has_motion = motion_percentage > self.threshold
        
        return has_motion, motion_percentage, fg_mask
    
    def is_playback_active(self, frame: np.ndarray, motion_threshold: float = 1.0) -> bool:
        """
        Determine if playback is active based on motion detection.
        
        Args:
            frame: Input frame
            motion_threshold: Minimum motion percentage to consider playback active
            
        Returns:
            True if playback appears active, False otherwise
        """
        has_motion, motion_percentage, _ = self.detect_motion(frame)
        return has_motion and motion_percentage >= motion_threshold
    
    def reset(self):
        """Reset the background subtractor (useful when scene changes significantly)."""
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=500, varThreshold=50, detectShadows=True
        )
        self.previous_frame = None

