# Scouty

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

**Scouty** is a modular robotics platform for building a mobile differential drive robot using Raspberry Pi and a microcontroller. The system features vision-based person tracking, finite state machine control, and robust motor control with safety features.

## 🎯 Features

- **Vision System**: Real-time person tracking using OpenCV and MediaPipe
- **Intelligent Control**: Finite state machine with Follow, Search, Approach, and Stop behaviors
- **Robust Communication**: UART protocol between Raspberry Pi and microcontroller
- **Safety First**: Emergency stop, watchdog timer, battery monitoring
- **Modular Design**: Clean separation of concerns for easy customization
- **Well-Documented**: Comprehensive documentation and examples

## 📁 Project Structure

```
Scouty/
├── vision/              # Computer vision (OpenCV, MediaPipe)
│   ├── camera.py        # Camera interface
│   ├── detector.py      # Object detection
│   ├── tracker.py       # Person tracking
│   └── processor.py     # Image processing utilities
├── control/             # Control logic and FSM
│   ├── fsm.py          # Finite State Machine
│   ├── controller.py    # Main controller
│   ├── behaviors.py     # State behaviors
│   └── motion.py        # Differential drive kinematics
├── mcu/                 # Microcontroller firmware
│   ├── main.cpp         # Main firmware
│   ├── motor_control.*  # Motor control
│   ├── uart_comm.*      # UART communication
│   └── safety.*         # Safety monitoring
├── communication/       # UART protocol
│   ├── uart_driver.py   # Python UART driver
│   └── protocol.md      # Protocol specification
├── hardware/            # Hardware designs
│   ├── pcb/            # PCB designs (placeholder)
│   └── cad/            # CAD files (placeholder)
├── tests/              # Test suite
│   ├── test_vision.py
│   ├── test_control.py
│   └── test_communication.py
└── docs/               # Documentation
    ├── getting_started.md
    ├── architecture.md
    └── ...
```

## 🚀 Quick Start

### Prerequisites

- Raspberry Pi 4 (4GB+ recommended)
- Microcontroller (Arduino/ESP32/STM32)
- Camera module
- Motor driver and DC motors
- Battery pack

### Installation

```bash
# Clone the repository
git clone https://github.com/AndrewFesenko/Scouty.git
cd Scouty

# Install Python dependencies
pip install -r vision/requirements.txt
pip install -r communication/requirements.txt

# Flash MCU firmware (using PlatformIO)
cd mcu
pio run --target upload
```

### Basic Usage

```python
from vision.camera import Camera
from vision.tracker import PersonTracker
from control.controller import RobotController
from communication.uart_driver import UARTDriver

# Initialize components
camera = Camera()
tracker = PersonTracker()
controller = RobotController()
uart = UARTDriver('/dev/ttyUSB0')

# Connect
camera.open()
uart.connect()
controller.start()

# Main loop
while True:
    # Get vision data
    success, frame = camera.read()
    if success:
        tracking_info = tracker.track(frame)
        
        # Update controller
        status = controller.update(tracking_info)
        
        # Send commands to MCU
        # ... (see full example in docs)
```

## 📖 Documentation

- [Getting Started Guide](docs/getting_started.md) - Installation and setup
- [System Architecture](docs/architecture.md) - Design overview
- [Communication Protocol](communication/protocol.md) - UART protocol details
- [API Reference](docs/api_reference.md) - Module documentation

## 🎮 Robot Behaviors

The robot operates in the following states:

- **IDLE**: Waiting for a person to detect
- **FOLLOW**: Actively following a detected person
- **APPROACH**: Moving closer when near the target
- **SEARCH**: Rotating to find a lost target
- **STOP**: Emergency stop or commanded halt

State transitions are automatic based on vision input and timeout conditions.

## 🔧 Hardware Setup

See [Hardware Setup Guide](docs/hardware_setup.md) for detailed assembly instructions.

### Minimum Requirements
- Raspberry Pi 3B+ or higher
- Arduino Uno/Nano or equivalent
- L298N motor driver
- 2x DC motors
- Camera module
- Battery pack (7.4V-12V)

### Recommended Setup
- Raspberry Pi 4 (4GB)
- ESP32 or STM32
- Advanced motor driver with current sensing
- Encoders for odometry
- IMU for better navigation

## 🧪 Testing

```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=vision --cov=control --cov=communication
```

## 🛡️ Safety Features

- **Hardware Emergency Stop**: Physical button for immediate shutdown
- **Watchdog Timer**: Automatic stop if no commands received (1s timeout)
- **Battery Monitoring**: Low voltage cutoff protection
- **Command Validation**: Checksums on all UART packets
- **Current Limiting**: Motor current protection

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenCV community for computer vision tools
- MediaPipe team for pose detection
- Arduino/PlatformIO communities for firmware support

## 📧 Contact

Andrew Fesenko - [@AndrewFesenko](https://github.com/AndrewFesenko)

Project Link: [https://github.com/AndrewFesenko/Scouty](https://github.com/AndrewFesenko/Scouty)

---

**Note**: This is a development platform. Always follow safety guidelines when working with robots and electricity. Test thoroughly before any autonomous operation.