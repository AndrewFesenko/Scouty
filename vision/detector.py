"""
Object detection module using OpenCV.
Provides detection capabilities for various objects and obstacles.
"""

import cv2
import numpy as np
from typing import List, Tuple, Optional


class ObjectDetector:
    """
    Object detector using OpenCV for obstacle and object detection.
    """
    
    def __init__(self):
        """Initialize object detector."""
        self.min_area = 500  # Minimum contour area to consider
        
    def detect_obstacles(self, frame: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect obstacles in the frame using contour detection.
        
        Args:
            frame: Input image frame (BGR format)
            
        Returns:
            List of bounding boxes (x, y, width, height)
        """
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Edge detection
        edges = cv2.Canny(blurred, 50, 150)
        
        # Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter and get bounding boxes
        obstacles = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.min_area:
                x, y, w, h = cv2.boundingRect(contour)
                obstacles.append((x, y, w, h))
        
        return obstacles
    
    def detect_color_blob(self, frame: np.ndarray, lower_color: np.ndarray, 
                         upper_color: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
        """
        Detect colored object blob in the frame.
        
        Args:
            frame: Input image frame (BGR format)
            lower_color: Lower HSV color bound
            upper_color: Upper HSV color bound
            
        Returns:
            Bounding box (x, y, width, height) or None if not found
        """
        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create mask
        mask = cv2.inRange(hsv, lower_color, upper_color)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            
            if cv2.contourArea(largest_contour) > self.min_area:
                x, y, w, h = cv2.boundingRect(largest_contour)
                return (x, y, w, h)
        
        return None
    
    def draw_detections(self, frame: np.ndarray, detections: List[Tuple[int, int, int, int]], 
                       color: Tuple[int, int, int] = (0, 255, 0)) -> np.ndarray:
        """
        Draw bounding boxes on frame.
        
        Args:
            frame: Input image frame
            detections: List of bounding boxes
            color: Color for bounding boxes (BGR)
            
        Returns:
            Frame with drawn detections
        """
        output = frame.copy()
        
        for (x, y, w, h) in detections:
            cv2.rectangle(output, (x, y), (x + w, y + h), color, 2)
        
        return output
