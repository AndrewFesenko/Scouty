# Getting Started with Scouty

This guide will help you set up and run the Scouty robot.

## Prerequisites

### Hardware Requirements
- Raspberry Pi 4 (4GB+ recommended)
- Microcontroller (Arduino/ESP32/STM32)
- Motor driver (L298N or similar)
- DC motors with encoders (optional)
- Camera (Raspberry Pi Camera or USB camera)
- Battery pack (3S LiPo or equivalent)
- Chassis and wheels

### Software Requirements
- Raspberry Pi OS (Bullseye or later)
- Python 3.7+
- Arduino IDE or PlatformIO (for MCU firmware)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AndrewFesenko/Scouty.git
cd Scouty
```

### 2. Install Python Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install vision dependencies
pip install -r vision/requirements.txt

# Install communication dependencies
pip install -r communication/requirements.txt

# Install test dependencies (optional)
pip install -r tests/requirements.txt
```

### 3. Flash MCU Firmware

#### Using Arduino IDE
1. Open `mcu/main.cpp` in Arduino IDE
2. Select your board (Tools → Board)
3. Select the correct port (Tools → Port)
4. Click Upload

#### Using PlatformIO
```bash
cd mcu
pio run --target upload
```

### 4. Configure UART Connection

Edit `/boot/config.txt` on Raspberry Pi:
```
enable_uart=1
dtoverlay=disable-bt
```

Reboot the Pi:
```bash
sudo reboot
```

### 5. Test the Setup

Run the test suite:
```bash
pytest tests/
```

## Basic Usage

### Running Vision System

```python
from vision.camera import Camera
from vision.tracker import PersonTracker

# Initialize camera
camera = Camera()
camera.open()

# Initialize tracker
tracker = PersonTracker()

# Process frames
while True:
    success, frame = camera.read()
    if success:
        tracking_info = tracker.track(frame)
        if tracking_info['detected']:
            print(f"Person detected at {tracking_info['center']}")
```

### Running Control System

```python
from control.controller import RobotController

# Initialize controller
controller = RobotController()
controller.start()

# Main loop
while controller.running:
    # Update with vision data
    status = controller.update(vision_data)
    print(f"State: {status['state']}")
```

### UART Communication

```python
from communication.uart_driver import UARTDriver

# Connect to MCU
with UARTDriver('/dev/ttyUSB0') as uart:
    # Set motor velocities
    uart.set_velocity(left_vel=100, right_vel=100)
    
    # Get status
    status = uart.get_status()
    print(f"Battery: {status['battery']}")
```

## Next Steps

- Read the [Architecture Documentation](architecture.md)
- Check [Hardware Setup Guide](hardware_setup.md)
- Review [API Reference](api_reference.md)
- Join the community discussions

## Troubleshooting

See [Troubleshooting Guide](troubleshooting.md) for common issues.
