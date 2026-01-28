"""
Main robot controller integrating FSM and vision.
Coordinates between state machine, vision system, and motor control.
"""

import time
from typing import Optional, Dict, Any
from .fsm import RobotFSM, RobotState
from .behaviors import FollowBehavior, SearchBehavior, ApproachBehavior


class RobotController:
    """
    Main robot controller.
    Integrates FSM, vision, and motor control.
    """
    
    def __init__(self, fsm: Optional[RobotFSM] = None):
        """
        Initialize robot controller.
        
        Args:
            fsm: Finite state machine (creates new one if None)
        """
        self.fsm = fsm if fsm else RobotFSM()
        
        # Behaviors
        self.follow_behavior = FollowBehavior()
        self.search_behavior = SearchBehavior()
        self.approach_behavior = ApproachBehavior()
        
        # Register state callbacks
        self.fsm.register_callback(RobotState.FOLLOW, self._follow_state)
        self.fsm.register_callback(RobotState.SEARCH, self._search_state)
        self.fsm.register_callback(RobotState.APPROACH, self._approach_state)
        self.fsm.register_callback(RobotState.STOP, self._stop_state)
        self.fsm.register_callback(RobotState.IDLE, self._idle_state)
        
        # Control parameters
        self.target_distance_threshold = 1.5  # Distance to switch to approach
        self.search_timeout = 10.0  # Seconds before giving up search
        
        self.running = False
        
    def _idle_state(self):
        """Idle state behavior."""
        # Do nothing, wait for person detection
        pass
    
    def _follow_state(self):
        """Follow state behavior."""
        # Execute follow behavior
        result = self.follow_behavior.execute()
        
        # Check for state transitions
        if not result.get('target_detected', False):
            # Lost target, switch to search
            self.fsm.transition(RobotState.SEARCH)
        elif result.get('distance_estimate', float('inf')) < self.target_distance_threshold:
            # Close to target, switch to approach
            self.fsm.transition(RobotState.APPROACH)
    
    def _search_state(self):
        """Search state behavior."""
        # Execute search behavior
        result = self.search_behavior.execute()
        
        # Check timeout
        if self.fsm.get_time_in_state() > self.search_timeout:
            # Give up, return to idle
            self.fsm.transition(RobotState.IDLE)
        elif result.get('target_found', False):
            # Found target, resume following
            self.fsm.transition(RobotState.FOLLOW)
    
    def _approach_state(self):
        """Approach state behavior."""
        # Execute approach behavior
        result = self.approach_behavior.execute()
        
        # Check if target moved away
        if result.get('distance_estimate', 0) > self.target_distance_threshold:
            # Target moved away, resume following
            self.fsm.transition(RobotState.FOLLOW)
    
    def _stop_state(self):
        """Stop state behavior."""
        # Send stop command to motors
        # This would interface with the MCU
        pass
    
    def update(self, vision_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update controller with sensor data.
        
        Args:
            vision_data: Data from vision system
            
        Returns:
            Control commands dictionary
        """
        # Update behaviors with vision data
        self.follow_behavior.update_data(vision_data)
        self.search_behavior.update_data(vision_data)
        self.approach_behavior.update_data(vision_data)
        
        # Execute current state
        self.fsm.execute()
        
        # Return current state and commands
        return {
            'state': self.fsm.get_state(),
            'time_in_state': self.fsm.get_time_in_state()
        }
    
    def start(self):
        """Start controller."""
        self.running = True
        self.fsm.reset()
    
    def stop(self):
        """Stop controller."""
        self.running = False
        self.fsm.emergency_stop()
    
    def emergency_stop(self):
        """Trigger emergency stop."""
        self.fsm.emergency_stop()
