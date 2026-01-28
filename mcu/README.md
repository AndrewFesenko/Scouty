# MCU Firmware

Microcontroller firmware for motor control and safety features.

## Target Hardware

- STM32 / Arduino / ESP32 (configurable)
- Motor driver (L298N, TB6612, or similar)
- Encoders (optional)
- Emergency stop button
- Battery voltage monitor

## Features

- PWM motor control
- Safety monitoring (voltage, temperature, emergency stop)
- UART communication with Raspberry Pi
- Encoder feedback (if available)
- Watchdog timer

## Building

### Arduino/PlatformIO

```bash
# Using PlatformIO
cd mcu
pio run

# Upload to board
pio run --target upload
```

### STM32 (using ARM GCC)

```bash
cd mcu/stm32
make
make flash
```

## Communication Protocol

See `../communication/protocol.md` for UART protocol specification.

## Safety Features

- Emergency stop input (hardware interrupt)
- Watchdog timer (auto-stop if no commands)
- Battery voltage monitoring
- Motor current limiting
- Thermal protection

## Pin Configuration

Default pin assignments (modify in `config.h`):

```
Motor A PWM:  Pin 5
Motor A DIR:  Pin 4
Motor B PWM:  Pin 6
Motor B DIR:  Pin 7
E-Stop:       Pin 2 (interrupt)
Voltage Mon:  A0 (analog)
```
