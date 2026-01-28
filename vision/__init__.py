"""
Vision module for Scouty robot.
Provides computer vision capabilities using OpenCV and MediaPipe.
"""

__version__ = "0.1.0"

from .camera import Camera
from .detector import ObjectDetector
from .tracker import PersonTracker

__all__ = ['Camera', 'ObjectDetector', 'PersonTracker']
