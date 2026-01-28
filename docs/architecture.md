# System Architecture

Overview of the Scouty robot software and hardware architecture.

## System Overview

```
┌─────────────────────────────────────────────────────┐
│              Raspberry Pi (Main Computer)            │
│                                                       │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐│
│  │   Vision    │  │   Control    │  │  Comm Layer ││
│  │  (OpenCV/   │→ │     FSM      │→ │    UART     ││
│  │  MediaPipe) │  │  Behaviors   │  │   Driver    ││
│  └─────────────┘  └──────────────┘  └──────┬──────┘│
│                                              │       │
└──────────────────────────────────────────────┼───────┘
                                               │ UART
                                               ↓
┌──────────────────────────────────────────────┼───────┐
│            Microcontroller (MCU)             │       │
│                                              │       │
│  ┌──────────────┐  ┌────────────┐  ┌────────┴─────┐│
│  │    Safety    │  │   Motor    │  │     UART     ││
│  │  Monitoring  │→ │  Control   │  │  Comm Layer  ││
│  └──────────────┘  └─────┬──────┘  └──────────────┘│
│                           │                          │
└───────────────────────────┼──────────────────────────┘
                            │ PWM
                            ↓
                    ┌───────────────┐
                    │ Motor Driver  │
                    └───────┬───────┘
                            │
                    ┌───────┴────────┐
                    │                │
                    ↓                ↓
                 Motor A         Motor B
```

## Component Descriptions

### Vision System (`vision/`)

Handles all computer vision tasks:
- **Camera Module**: Frame capture from Pi Camera or USB camera
- **Object Detector**: OpenCV-based obstacle and object detection
- **Person Tracker**: MediaPipe pose detection for person following
- **Image Processor**: Preprocessing and utilities

**Key Technologies**: OpenCV, MediaPipe, NumPy

### Control System (`control/`)

Implements robot behavior and decision-making:
- **Finite State Machine (FSM)**: State management and transitions
- **Controller**: Main control loop coordinator
- **Behaviors**: State-specific logic (Follow, Search, Approach, Stop)
- **Motion Planner**: Differential drive kinematics

**States**:
- IDLE: Waiting for target
- FOLLOW: Tracking and following person
- APPROACH: Moving closer to target
- SEARCH: Looking for lost target
- STOP: Emergency stop or commanded halt

### Communication Layer (`communication/`)

UART protocol for Pi ↔ MCU communication:
- **Protocol**: Binary packet-based with checksums
- **Commands**: Velocity control, stop, status requests
- **Status Updates**: Battery, emergency stop, motor current

**Baud Rate**: 115200

### MCU Firmware (`mcu/`)

Low-level motor control and safety:
- **Motor Control**: PWM generation for motor driver
- **Safety Monitoring**: Battery voltage, emergency stop
- **UART Handler**: Protocol implementation
- **Watchdog**: Automatic stop on communication loss

**Supported Platforms**: Arduino, ESP32, STM32

## Data Flow

### Normal Operation

1. **Vision**: Camera captures frame → Tracker detects person → Position + distance
2. **Control**: FSM processes vision data → Behavior generates velocities
3. **Communication**: UART sends velocity commands to MCU
4. **MCU**: Receives commands → Safety checks → PWM to motors
5. **Status**: MCU sends status back to Pi periodically

### Emergency Stop

Hardware E-stop button → MCU interrupt → Motors stop immediately → Pi notified

## Communication Protocol

### Command Packet Structure
```
[START_BYTE][LENGTH][DATA...][CHECKSUM]
```

### Commands (Pi → MCU)
- `0x01`: Set Velocity (left, right)
- `0x02`: Stop
- `0x03`: Reset E-Stop
- `0x04`: Get Status

### Status (MCU → Pi)
- `0x10`: Status Update (battery, e-stop, current)

See [protocol.md](../communication/protocol.md) for details.

## State Machine

```
      ┌─────┐
      │IDLE │
      └──┬──┘
         │ person detected
         ↓
      ┌──────┐      close
      │FOLLOW│ ─────────→ ┌──────────┐
      └──┬───┘            │ APPROACH │
         │                └──────────┘
         │ lost target
         ↓
      ┌───────┐    timeout
      │SEARCH │ ────────→ IDLE
      └───────┘
           │ found
           └────→ FOLLOW

   [Any State] ─ emergency ─→ STOP
```

## Safety Features

1. **Hardware E-Stop**: Physical button for immediate stop
2. **Watchdog Timer**: Auto-stop if no commands for 1 second
3. **Battery Monitor**: Voltage monitoring, low battery cutoff
4. **Command Validation**: Checksum verification on all packets

## Extensibility

The architecture is modular and extensible:
- Add new behaviors by extending `Behavior` class
- Add new states to FSM with transition rules
- Extend vision with additional detectors
- Add sensors via MCU GPIO or I2C

## Performance

- Vision processing: 15-30 FPS (depending on Pi model)
- Control loop: 50-100 Hz
- UART communication: Up to 50 Hz command rate
- MCU loop: 100 Hz

## Hardware Requirements

### Minimum
- Raspberry Pi 3B+
- Arduino Uno/Nano
- Basic motor driver

### Recommended
- Raspberry Pi 4 (4GB)
- ESP32 or STM32
- Advanced motor driver with current sensing
