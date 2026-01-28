"""
Motion planning and path generation utilities.
Provides differential drive kinematics and path planning.
"""

import math
from typing import Tuple


class DifferentialDrive:
    """
    Differential drive kinematics for two-wheeled robot.
    """
    
    def __init__(self, wheel_base: float = 0.2, wheel_radius: float = 0.05):
        """
        Initialize differential drive.
        
        Args:
            wheel_base: Distance between wheels (meters)
            wheel_radius: Radius of wheels (meters)
        """
        self.wheel_base = wheel_base
        self.wheel_radius = wheel_radius
        
    def inverse_kinematics(self, linear_vel: float, 
                          angular_vel: float) -> Tuple[float, float]:
        """
        Convert linear and angular velocities to wheel velocities.
        
        Args:
            linear_vel: Forward velocity (m/s)
            angular_vel: Angular velocity (rad/s)
            
        Returns:
            Tuple of (left_wheel_vel, right_wheel_vel) in rad/s
        """
        # Calculate wheel velocities
        left_vel = (linear_vel - (angular_vel * self.wheel_base / 2)) / self.wheel_radius
        right_vel = (linear_vel + (angular_vel * self.wheel_base / 2)) / self.wheel_radius
        
        return (left_vel, right_vel)
    
    def forward_kinematics(self, left_wheel_vel: float, 
                          right_wheel_vel: float) -> Tuple[float, float]:
        """
        Convert wheel velocities to robot velocities.
        
        Args:
            left_wheel_vel: Left wheel velocity (rad/s)
            right_wheel_vel: Right wheel velocity (rad/s)
            
        Returns:
            Tuple of (linear_vel, angular_vel)
        """
        # Calculate robot velocities
        linear_vel = self.wheel_radius * (left_wheel_vel + right_wheel_vel) / 2
        angular_vel = self.wheel_radius * (right_wheel_vel - left_wheel_vel) / self.wheel_base
        
        return (linear_vel, angular_vel)
    
    def limit_velocities(self, left_vel: float, right_vel: float,
                        max_vel: float = 10.0) -> Tuple[float, float]:
        """
        Limit wheel velocities to maximum.
        
        Args:
            left_vel: Left wheel velocity
            right_vel: Right wheel velocity
            max_vel: Maximum wheel velocity (rad/s)
            
        Returns:
            Limited (left_vel, right_vel)
        """
        # Find scaling factor if needed
        max_wheel = max(abs(left_vel), abs(right_vel))
        
        if max_wheel > max_vel:
            scale = max_vel / max_wheel
            left_vel *= scale
            right_vel *= scale
        
        return (left_vel, right_vel)


class PathPlanner:
    """
    Simple path planning utilities.
    """
    
    @staticmethod
    def point_to_point(current_x: float, current_y: float, current_theta: float,
                      target_x: float, target_y: float) -> Tuple[float, float]:
        """
        Calculate velocities to move from current position to target.
        
        Args:
            current_x: Current x position
            current_y: Current y position
            current_theta: Current orientation (radians)
            target_x: Target x position
            target_y: Target y position
            
        Returns:
            Tuple of (linear_velocity, angular_velocity)
        """
        # Calculate distance and angle to target
        dx = target_x - current_x
        dy = target_y - current_y
        
        distance = math.sqrt(dx**2 + dy**2)
        target_angle = math.atan2(dy, dx)
        
        # Calculate angle error
        angle_error = target_angle - current_theta
        
        # Normalize angle to [-pi, pi]
        angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))
        
        # Simple controller
        angular_velocity = 2.0 * angle_error  # Proportional control
        linear_velocity = 0.5 * distance if abs(angle_error) < 0.5 else 0.0
        
        return (linear_velocity, angular_velocity)
