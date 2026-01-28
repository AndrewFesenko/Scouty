"""
Tests for control system components.
"""

import pytest
from control.fsm import RobotFSM, RobotState
from control.controller import RobotController
from control.behaviors import FollowBehavior, SearchBehavior


class TestRobotFSM:
    """Tests for Finite State Machine."""
    
    def test_fsm_initialization(self):
        """Test FSM initialization."""
        fsm = RobotFSM()
        assert fsm.get_state() == RobotState.IDLE
        assert fsm.previous_state is None
    
    def test_valid_transition(self):
        """Test valid state transition."""
        fsm = RobotFSM()
        result = fsm.transition(RobotState.FOLLOW)
        assert result is True
        assert fsm.get_state() == RobotState.FOLLOW
        assert fsm.previous_state == RobotState.IDLE
    
    def test_invalid_transition(self):
        """Test invalid state transition."""
        fsm = RobotFSM()
        # IDLE cannot transition directly to SEARCH
        result = fsm.transition(RobotState.SEARCH)
        assert result is False
        assert fsm.get_state() == RobotState.IDLE
    
    def test_forced_transition(self):
        """Test forced transition (emergency stop)."""
        fsm = RobotFSM()
        fsm.transition(RobotState.FOLLOW)
        
        # Force transition to STOP (emergency)
        result = fsm.transition(RobotState.STOP, force=True)
        assert result is True
        assert fsm.get_state() == RobotState.STOP
    
    def test_emergency_stop(self):
        """Test emergency stop."""
        fsm = RobotFSM()
        fsm.transition(RobotState.FOLLOW)
        fsm.emergency_stop()
        assert fsm.get_state() == RobotState.STOP
    
    def test_reset(self):
        """Test FSM reset."""
        fsm = RobotFSM()
        fsm.transition(RobotState.FOLLOW)
        fsm.reset()
        assert fsm.get_state() == RobotState.IDLE
        assert fsm.previous_state is None


class TestRobotController:
    """Tests for Robot Controller."""
    
    def test_controller_initialization(self):
        """Test controller initialization."""
        controller = RobotController()
        assert controller.fsm is not None
        assert controller.fsm.get_state() == RobotState.IDLE
    
    def test_start_stop(self):
        """Test controller start and stop."""
        controller = RobotController()
        controller.start()
        assert controller.running is True
        assert controller.fsm.get_state() == RobotState.IDLE
        
        controller.stop()
        assert controller.running is False
        assert controller.fsm.get_state() == RobotState.STOP


class TestFollowBehavior:
    """Tests for Follow Behavior."""
    
    def test_follow_no_target(self):
        """Test follow behavior without target."""
        behavior = FollowBehavior()
        behavior.update_data({'detected': False})
        result = behavior.execute()
        
        assert result['target_detected'] is False
        assert result['linear_velocity'] == 0.0
        assert result['angular_velocity'] == 0.0
    
    def test_follow_with_target(self):
        """Test follow behavior with target."""
        behavior = FollowBehavior()
        behavior.update_data({
            'detected': True,
            'center': (320, 240),  # Centered
            'distance_estimate': 2.0
        })
        result = behavior.execute()
        
        assert result['target_detected'] is True
        assert result['linear_velocity'] > 0  # Should move forward


class TestSearchBehavior:
    """Tests for Search Behavior."""
    
    def test_search_rotating(self):
        """Test search behavior is rotating."""
        behavior = SearchBehavior()
        behavior.update_data({'detected': False})
        result = behavior.execute()
        
        assert result['target_found'] is False
        assert result['angular_velocity'] != 0  # Should be rotating
        assert result['linear_velocity'] == 0
    
    def test_search_target_found(self):
        """Test search behavior when target found."""
        behavior = SearchBehavior()
        behavior.update_data({'detected': True})
        result = behavior.execute()
        
        assert result['target_found'] is True


if __name__ == '__main__':
    pytest.main([__file__])
