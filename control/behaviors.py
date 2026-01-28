"""
Behavior implementations for different robot states.
Each behavior encapsulates the logic for a specific state.
"""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class Behavior(ABC):
    """
    Abstract base class for robot behaviors.
    """
    
    def __init__(self):
        """Initialize behavior."""
        self.data: Dict[str, Any] = {}
    
    def update_data(self, data: Dict[str, Any]):
        """
        Update behavior with new sensor data.
        
        Args:
            data: Sensor data dictionary
        """
        self.data = data
    
    @abstractmethod
    def execute(self) -> Dict[str, Any]:
        """
        Execute behavior.
        
        Returns:
            Result dictionary with behavior output
        """
        pass


class FollowBehavior(Behavior):
    """
    Follow behavior - track and follow detected person.
    """
    
    # Control parameters
    ANGULAR_GAIN = 0.01  # Proportional gain for angular velocity control
    LINEAR_VELOCITY = 0.3  # Forward velocity when centered (m/s)
    
    def __init__(self, frame_width: int = 640):
        """
        Initialize follow behavior.
        
        Args:
            frame_width: Camera frame width in pixels (default 640)
        """
        super().__init__()
        self.center_tolerance = 50  # pixels from center
        self.frame_center_x = frame_width // 2
        
    def execute(self) -> Dict[str, Any]:
        """
        Execute follow behavior.
        
        Returns:
            Dictionary with motor commands and status
        """
        result = {
            'target_detected': False,
            'linear_velocity': 0.0,
            'angular_velocity': 0.0,
            'distance_estimate': None
        }
        
        # Check if target is detected
        if self.data.get('detected', False):
            result['target_detected'] = True
            
            # Get target position
            center = self.data.get('center')
            distance = self.data.get('distance_estimate')
            
            if center:
                # Calculate error from center
                error = center[0] - self.frame_center_x
                
                # Calculate angular velocity based on error (proportional control)
                if abs(error) > self.center_tolerance:
                    # Turn to center target
                    result['angular_velocity'] = -error * self.ANGULAR_GAIN
                
                # Move forward if target is centered
                if abs(error) < self.center_tolerance:
                    result['linear_velocity'] = self.LINEAR_VELOCITY
                
                result['distance_estimate'] = distance
        
        return result


class SearchBehavior(Behavior):
    """
    Search behavior - rotate and look for target when lost.
    """
    
    def __init__(self):
        """Initialize search behavior."""
        super().__init__()
        self.search_angular_velocity = 0.5  # rad/s
        
    def execute(self) -> Dict[str, Any]:
        """
        Execute search behavior.
        
        Returns:
            Dictionary with motor commands and status
        """
        result = {
            'target_found': False,
            'linear_velocity': 0.0,
            'angular_velocity': self.search_angular_velocity
        }
        
        # Check if target reappeared
        if self.data.get('detected', False):
            result['target_found'] = True
            result['angular_velocity'] = 0.0
        
        return result


class ApproachBehavior(Behavior):
    """
    Approach behavior - carefully move closer to target.
    """
    
    # Control parameters
    ANGULAR_GAIN = 0.005  # Gentler proportional gain for approach
    
    def __init__(self, frame_width: int = 640):
        """
        Initialize approach behavior.
        
        Args:
            frame_width: Camera frame width in pixels (default 640)
        """
        super().__init__()
        self.approach_velocity = 0.1  # Slower velocity for approach
        self.stop_distance = 0.5  # Stop when very close
        self.frame_center_x = frame_width // 2
        
    def execute(self) -> Dict[str, Any]:
        """
        Execute approach behavior.
        
        Returns:
            Dictionary with motor commands and status
        """
        result = {
            'linear_velocity': 0.0,
            'angular_velocity': 0.0,
            'distance_estimate': None
        }
        
        # Get distance estimate
        distance = self.data.get('distance_estimate')
        
        if distance and distance > self.stop_distance:
            result['linear_velocity'] = self.approach_velocity
            result['distance_estimate'] = distance
            
            # Keep target centered
            center = self.data.get('center')
            if center:
                error = center[0] - self.frame_center_x
                result['angular_velocity'] = -error * self.ANGULAR_GAIN  # Gentle correction
        
        return result


class StopBehavior(Behavior):
    """
    Stop behavior - halt all motion.
    """
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute stop behavior.
        
        Returns:
            Dictionary with zero velocities
        """
        return {
            'linear_velocity': 0.0,
            'angular_velocity': 0.0
        }
