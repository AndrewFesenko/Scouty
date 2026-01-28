"""
Tests for vision system components.
"""

import pytest
import numpy as np
from unittest.mock import Mock, patch


class TestCamera:
    """Tests for Camera class."""
    
    @patch('cv2.VideoCapture')
    def test_camera_initialization(self, mock_video_capture):
        """Test camera initialization."""
        from vision.camera import Camera
        
        camera = Camera(camera_id=0, width=640, height=480)
        assert camera.camera_id == 0
        assert camera.width == 640
        assert camera.height == 480
        assert not camera.is_open
    
    @patch('cv2.VideoCapture')
    def test_camera_open(self, mock_video_capture):
        """Test camera open."""
        from vision.camera import Camera
        
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_video_capture.return_value = mock_cap
        
        camera = Camera()
        result = camera.open()
        
        assert result is True
        assert camera.is_open
    
    @patch('cv2.VideoCapture')
    def test_camera_read(self, mock_video_capture):
        """Test camera read."""
        from vision.camera import Camera
        
        mock_cap = Mock()
        mock_cap.isOpened.return_value = True
        mock_cap.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
        mock_video_capture.return_value = mock_cap
        
        camera = Camera()
        camera.open()
        success, frame = camera.read()
        
        assert success is True
        assert frame is not None
        assert frame.shape == (480, 640, 3)


class TestObjectDetector:
    """Tests for ObjectDetector class."""
    
    def test_detector_initialization(self):
        """Test detector initialization."""
        from vision.detector import ObjectDetector
        
        detector = ObjectDetector()
        assert detector.min_area == 500
    
    def test_detect_obstacles_empty_frame(self):
        """Test obstacle detection on empty frame."""
        from vision.detector import ObjectDetector
        
        detector = ObjectDetector()
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        obstacles = detector.detect_obstacles(frame)
        
        assert isinstance(obstacles, list)
    
    def test_detect_color_blob_no_match(self):
        """Test color blob detection with no match."""
        from vision.detector import ObjectDetector
        
        detector = ObjectDetector()
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        lower = np.array([0, 100, 100])
        upper = np.array([10, 255, 255])
        
        result = detector.detect_color_blob(frame, lower, upper)
        assert result is None


if __name__ == '__main__':
    pytest.main([__file__])
