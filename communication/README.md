# Communication Module

UART communication between Raspberry Pi and microcontroller.

## Protocol

See `protocol.md` for detailed protocol specification.

## Python Implementation

### Installation

```bash
pip install pyserial
```

### Usage

```python
from communication.uart_driver import UARTDriver

# Initialize UART
uart = UARTDriver('/dev/ttyUSB0', baudrate=115200)

# Send velocity command
uart.set_velocity(left_vel=100, right_vel=100)

# Stop motors
uart.stop()

# Get status
status = uart.get_status()
print(f"Battery: {status['battery']}, E-Stop: {status['estop']}")

# Close connection
uart.close()
```

## Files

- `protocol.md` - Protocol specification
- `uart_driver.py` - Python UART driver for Raspberry Pi
- `__init__.py` - Module initialization
