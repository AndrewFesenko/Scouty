# Control System

This module implements the robot control logic using a finite state machine (FSM).

## States

The robot operates in the following states:

- **IDLE** - Waiting for commands
- **FOLLOW** - Following a detected person
- **APPROACH** - Moving closer to target
- **STOP** - Stopped (safety or command)
- **SEARCH** - Searching for target when lost

## State Transitions

```
IDLE -> FOLLOW (person detected)
FOLLOW -> APPROACH (person close, distance < threshold)
FOLLOW -> SEARCH (person lost)
SEARCH -> FOLLOW (person found)
SEARCH -> IDLE (timeout)
ANY -> STOP (emergency stop or safety trigger)
```

## Usage

```python
from control.fsm import RobotFSM
from control.controller import RobotController

# Initialize FSM
fsm = RobotFSM()

# Create controller
controller = RobotController(fsm)

# Run control loop
controller.run()
```

## Modules

- `fsm.py` - Finite State Machine implementation
- `controller.py` - Main robot controller
- `motion.py` - Motion planning and path generation
- `behaviors.py` - Behavior implementations for each state
