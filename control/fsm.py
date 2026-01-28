"""
Finite State Machine for robot control.
Manages state transitions and behavior orchestration.
"""

from enum import Enum, auto
from typing import Optional, Callable, Dict
import time


class RobotState(Enum):
    """Robot states enumeration."""
    IDLE = auto()
    FOLLOW = auto()
    APPROACH = auto()
    STOP = auto()
    SEARCH = auto()


class RobotFSM:
    """
    Finite State Machine for robot behavior control.
    Manages states and transitions based on sensor input and events.
    """
    
    def __init__(self):
        """Initialize FSM."""
        self.current_state = RobotState.IDLE
        self.previous_state = None
        self.state_start_time = time.time()
        
        # State callbacks
        self.state_callbacks: Dict[RobotState, Callable] = {}
        
        # Transition rules
        self.transitions = {
            RobotState.IDLE: [RobotState.FOLLOW, RobotState.STOP],
            RobotState.FOLLOW: [RobotState.APPROACH, RobotState.SEARCH, 
                               RobotState.STOP, RobotState.IDLE],
            RobotState.APPROACH: [RobotState.FOLLOW, RobotState.STOP, 
                                 RobotState.IDLE],
            RobotState.SEARCH: [RobotState.FOLLOW, RobotState.IDLE, 
                               RobotState.STOP],
            RobotState.STOP: [RobotState.IDLE, RobotState.FOLLOW]
        }
        
    def register_callback(self, state: RobotState, callback: Callable):
        """
        Register a callback function for a state.
        
        Args:
            state: Robot state
            callback: Function to call when in this state
        """
        self.state_callbacks[state] = callback
    
    def can_transition(self, new_state: RobotState) -> bool:
        """
        Check if transition to new state is allowed.
        
        Args:
            new_state: Target state
            
        Returns:
            True if transition is allowed
        """
        return new_state in self.transitions.get(self.current_state, [])
    
    def transition(self, new_state: RobotState, force: bool = False) -> bool:
        """
        Transition to a new state.
        
        Args:
            new_state: Target state
            force: If True, bypass transition rules (for emergency stop)
            
        Returns:
            True if transition successful
        """
        if force or self.can_transition(new_state):
            self.previous_state = self.current_state
            self.current_state = new_state
            self.state_start_time = time.time()
            return True
        return False
    
    def get_state(self) -> RobotState:
        """
        Get current state.
        
        Returns:
            Current robot state
        """
        return self.current_state
    
    def get_time_in_state(self) -> float:
        """
        Get time elapsed in current state.
        
        Returns:
            Time in seconds
        """
        return time.time() - self.state_start_time
    
    def execute(self):
        """
        Execute callback for current state if registered.
        """
        callback = self.state_callbacks.get(self.current_state)
        if callback:
            callback()
    
    def emergency_stop(self):
        """
        Perform emergency stop (forced transition).
        """
        self.transition(RobotState.STOP, force=True)
    
    def reset(self):
        """
        Reset FSM to initial state.
        """
        self.transition(RobotState.IDLE, force=True)
        self.previous_state = None
