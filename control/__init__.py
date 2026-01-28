"""
Control module for Scouty robot.
Provides finite state machine and behavior control.
"""

__version__ = "0.1.0"

from .fsm import RobotFSM, RobotState
from .controller import RobotController
from .motion import DifferentialDrive, PathPlanner

__all__ = ['RobotFSM', 'RobotState', 'RobotController', 
           'DifferentialDrive', 'PathPlanner']
