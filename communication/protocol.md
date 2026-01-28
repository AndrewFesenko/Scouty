# Communication Protocol

UART communication protocol between Raspberry Pi and Microcontroller.

## Physical Layer

- **Baud Rate:** 115200
- **Data Bits:** 8
- **Parity:** None
- **Stop Bits:** 1
- **Flow Control:** None

## Packet Structure

All packets follow this structure:

```
[START_BYTE][LENGTH][DATA...][CHECKSUM]
```

- **START_BYTE:** `0xAA` (packet delimiter)
- **LENGTH:** 1 byte (number of data bytes, 1-255)
- **DATA:** Variable length payload
- **CHECKSUM:** 1 byte (simple sum of all data bytes)

## Command Packets (Pi → MCU)

### Set Velocity (0x01)

Set motor velocities.

```
DATA: [0x01][LEFT_VEL_H][LEFT_VEL_L][RIGHT_VEL_H][RIGHT_VEL_L]
```

- `LEFT_VEL`: 16-bit signed integer (-255 to +255)
- `RIGHT_VEL`: 16-bit signed integer (-255 to +255)
- Positive = forward, Negative = reverse

### Stop (0x02)

Emergency stop all motors.

```
DATA: [0x02]
```

### Reset Emergency Stop (0x03)

Reset emergency stop condition (if safe).

```
DATA: [0x03]
```

### Get Status (0x04)

Request status update from MCU.

```
DATA: [0x04]
```

## Status Packets (MCU → Pi)

### Status Update (0x10)

Periodic status information.

```
DATA: [0x10][BATTERY][ESTOP][CURRENT_L][CURRENT_R]
```

- `BATTERY`: Battery voltage (scaled 0-255)
- `ESTOP`: Emergency stop status (0=normal, 1=stopped)
- `CURRENT_L`: Left motor current (scaled 0-255)
- `CURRENT_R`: Right motor current (scaled 0-255)

## Error Handling

- Invalid checksum → packet discarded
- Watchdog timeout (1 second) → motors stop automatically
- E-stop triggered → all commands ignored until reset

## Example Implementations

See:
- `uart_comm.cpp` - MCU implementation
- `../communication/uart_driver.py` - Python implementation

## Timing

- Command rate: Up to 50 Hz recommended
- Status updates: 10 Hz from MCU
- Watchdog timeout: 1000 ms
