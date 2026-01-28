"""
Camera interface module for Raspberry Pi camera.
Handles video capture and frame acquisition.
"""

import cv2
import numpy as np
from typing import Optional, Tuple


class Camera:
    """
    Camera interface for capturing video frames.
    Supports both USB cameras and Raspberry Pi Camera Module.
    """
    
    def __init__(self, camera_id: int = 0, width: int = 640, height: int = 480):
        """
        Initialize camera.
        
        Args:
            camera_id: Camera device ID (default 0)
            width: Frame width in pixels
            height: Frame height in pixels
        """
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.cap = None
        self.is_open = False
        
    def open(self) -> bool:
        """
        Open camera connection.
        
        Returns:
            True if camera opened successfully, False otherwise
        """
        self.cap = cv2.VideoCapture(self.camera_id)
        
        if self.cap.isOpened():
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.is_open = True
            return True
        
        return False
    
    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Read a frame from the camera.
        
        Returns:
            Tuple of (success, frame) where success is bool and frame is numpy array
        """
        if not self.is_open or self.cap is None:
            return False, None
        
        ret, frame = self.cap.read()
        return ret, frame
    
    def close(self):
        """Release camera resources."""
        if self.cap is not None:
            self.cap.release()
            self.is_open = False
    
    def __enter__(self):
        """Context manager entry."""
        self.open()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
