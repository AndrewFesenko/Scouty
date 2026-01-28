"""
Simple example: FSM and controller test.
"""

from control.fsm import RobotFSM, RobotState
from control.controller import RobotController
import time


def main():
    """Test FSM and controller."""
    print("Starting control system test...\n")
    
    # Create FSM
    fsm = RobotFSM()
    
    # Test transitions
    print("Testing FSM transitions:")
    print(f"Initial state: {fsm.get_state()}")
    
    # IDLE -> FOLLOW
    fsm.transition(RobotState.FOLLOW)
    print(f"After transition to FOLLOW: {fsm.get_state()}")
    
    # FOLLOW -> SEARCH
    fsm.transition(RobotState.SEARCH)
    print(f"After transition to SEARCH: {fsm.get_state()}")
    
    # Emergency stop
    fsm.emergency_stop()
    print(f"After emergency stop: {fsm.get_state()}")
    
    # Reset
    fsm.reset()
    print(f"After reset: {fsm.get_state()}\n")
    
    # Test controller
    print("Testing controller with simulated vision data:")
    controller = RobotController()
    controller.start()
    
    # Simulate detection
    for i in range(5):
        vision_data = {
            'detected': True,
            'center': (320, 240),
            'distance_estimate': 2.0
        }
        
        status = controller.update(vision_data)
        print(f"Frame {i+1}: State={status['state'].name}, "
              f"Time={status['time_in_state']:.1f}s")
        time.sleep(0.1)
    
    # Simulate loss of target
    print("\nTarget lost, switching to search:")
    for i in range(3):
        vision_data = {'detected': False}
        status = controller.update(vision_data)
        print(f"Frame {i+6}: State={status['state'].name}, "
              f"Time={status['time_in_state']:.1f}s")
        time.sleep(0.1)
    
    controller.stop()
    print("\nControl system test completed")


if __name__ == '__main__':
    main()
