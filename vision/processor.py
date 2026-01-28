"""
Image processing utilities for vision pipeline.
Provides common image processing operations.
"""

import cv2
import numpy as np
from typing import Tuple


class ImageProcessor:
    """
    Utilities for image preprocessing and manipulation.
    """
    
    @staticmethod
    def resize_frame(frame: np.ndarray, width: int, height: int) -> np.ndarray:
        """
        Resize frame to specified dimensions.
        
        Args:
            frame: Input image frame
            width: Target width
            height: Target height
            
        Returns:
            Resized frame
        """
        return cv2.resize(frame, (width, height))
    
    @staticmethod
    def normalize_frame(frame: np.ndarray) -> np.ndarray:
        """
        Normalize frame values to 0-1 range.
        
        Args:
            frame: Input image frame
            
        Returns:
            Normalized frame
        """
        return frame.astype(np.float32) / 255.0
    
    @staticmethod
    def enhance_contrast(frame: np.ndarray) -> np.ndarray:
        """
        Enhance frame contrast using histogram equalization.
        
        Args:
            frame: Input image frame (grayscale or BGR)
            
        Returns:
            Contrast-enhanced frame
        """
        if len(frame.shape) == 2:
            # Grayscale
            return cv2.equalizeHist(frame)
        else:
            # Color image - convert to YCrCb and equalize Y channel
            ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)
            ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
            return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)
    
    @staticmethod
    def apply_bilateral_filter(frame: np.ndarray, d: int = 9, 
                               sigma_color: int = 75, 
                               sigma_space: int = 75) -> np.ndarray:
        """
        Apply bilateral filter for edge-preserving smoothing.
        
        Args:
            frame: Input image frame
            d: Diameter of pixel neighborhood
            sigma_color: Filter sigma in color space
            sigma_space: Filter sigma in coordinate space
            
        Returns:
            Filtered frame
        """
        return cv2.bilateralFilter(frame, d, sigma_color, sigma_space)
    
    @staticmethod
    def crop_center(frame: np.ndarray, crop_width: int, crop_height: int) -> np.ndarray:
        """
        Crop center region of frame.
        
        Args:
            frame: Input image frame
            crop_width: Width of crop
            crop_height: Height of crop
            
        Returns:
            Cropped frame
            
        Raises:
            ValueError: If crop dimensions exceed frame dimensions
        """
        h, w = frame.shape[:2]
        
        # Validate crop dimensions
        if crop_width > w or crop_height > h:
            raise ValueError(f"Crop dimensions ({crop_width}x{crop_height}) "
                           f"exceed frame dimensions ({w}x{h})")
        
        start_x = (w - crop_width) // 2
        start_y = (h - crop_height) // 2
        
        return frame[start_y:start_y + crop_height, start_x:start_x + crop_width]
