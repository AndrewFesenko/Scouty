# Hardware - PCB Design

Placeholder for custom PCB designs.

## Planned Boards

### Motor Driver Board
- Dual H-bridge motor driver
- Current sensing
- Battery voltage monitoring
- Emergency stop input
- MCU interface (headers)

### Sensor Board
- IMU (gyroscope, accelerometer)
- Ultrasonic sensors
- IR sensors
- Voltage regulators

### Main Controller Board (optional)
- Raspberry Pi mounting
- MCU (STM32/ESP32)
- Power management
- Sensor interfaces

## Tools

Recommended PCB design tools:
- KiCad (open source)
- Eagle
- Altium Designer

## Files

Place your PCB design files here:
- Schematics (.sch)
- PCB layouts (.kicad_pcb, .brd)
- Gerber files (for manufacturing)
- Bill of Materials (BOM)

## Design Guidelines

- Use proper trace widths for motor currents (>2mm for 2A+)
- Include test points for debugging
- Add mounting holes for mechanical integration
- Consider EMI/EMC (bypass capacitors, ground planes)
- Label all connectors clearly
