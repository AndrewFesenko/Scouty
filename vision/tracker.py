"""
Person tracking module using MediaPipe.
Provides person detection and tracking capabilities.
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import Optional, Tuple, Dict


class PersonTracker:
    """
    Person tracker using MediaPipe pose detection.
    Tracks person position for follow behavior.
    """
    
    def __init__(self, min_detection_confidence: float = 0.5, 
                 min_tracking_confidence: float = 0.5):
        """
        Initialize person tracker.
        
        Args:
            min_detection_confidence: Minimum confidence for detection
            min_tracking_confidence: Minimum confidence for tracking
        """
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
        self.person_detected = False
        self.person_position = None
        
    def track(self, frame: np.ndarray) -> Dict:
        """
        Track person in the frame.
        
        Args:
            frame: Input image frame (BGR format)
            
        Returns:
            Dictionary containing tracking information:
            - detected: bool
            - center: (x, y) tuple or None
            - distance_estimate: float or None (based on shoulder width)
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame
        results = self.pose.process(rgb_frame)
        
        tracking_info = {
            'detected': False,
            'center': None,
            'distance_estimate': None,
            'landmarks': None
        }
        
        if results.pose_landmarks:
            tracking_info['detected'] = True
            tracking_info['landmarks'] = results.pose_landmarks
            
            # Calculate center position (using shoulders and hips)
            landmarks = results.pose_landmarks.landmark
            h, w, _ = frame.shape
            
            # Get key points
            left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
            
            # Calculate center
            center_x = int((left_shoulder.x + right_shoulder.x) / 2 * w)
            center_y = int((left_shoulder.y + right_shoulder.y) / 2 * h)
            
            tracking_info['center'] = (center_x, center_y)
            
            # Estimate distance based on shoulder width (pixels)
            shoulder_width = abs(left_shoulder.x - right_shoulder.x) * w
            
            # Simple inverse relationship for distance estimation
            if shoulder_width > 0:
                # Normalized distance (larger width = closer)
                tracking_info['distance_estimate'] = 100.0 / shoulder_width
            
            self.person_detected = True
            self.person_position = tracking_info['center']
        else:
            self.person_detected = False
            self.person_position = None
        
        return tracking_info
    
    def draw_tracking(self, frame: np.ndarray, tracking_info: Dict) -> np.ndarray:
        """
        Draw tracking visualization on frame.
        
        Args:
            frame: Input image frame
            tracking_info: Tracking information from track()
            
        Returns:
            Frame with tracking visualization
        """
        output = frame.copy()
        
        if tracking_info['detected'] and tracking_info['landmarks']:
            # Draw pose landmarks
            self.mp_drawing.draw_landmarks(
                output,
                tracking_info['landmarks'],
                self.mp_pose.POSE_CONNECTIONS
            )
            
            # Draw center point
            if tracking_info['center']:
                cv2.circle(output, tracking_info['center'], 10, (0, 255, 0), -1)
                
                # Draw distance text
                if tracking_info['distance_estimate']:
                    text = f"Dist: {tracking_info['distance_estimate']:.2f}"
                    cv2.putText(output, text, (10, 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return output
    
    def close(self):
        """Release resources."""
        self.pose.close()
