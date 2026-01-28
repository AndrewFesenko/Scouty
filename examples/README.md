# Scouty Examples

Example scripts demonstrating Scouty robot functionality.

## Available Examples

### 1. Vision Test (`vision_test.py`)

Test camera and person tracking.

```bash
python3 examples/vision_test.py
```

**Features:**
- Camera capture
- Person detection
- Real-time visualization
- Press 'q' to quit

**Requirements:**
- Camera connected
- OpenCV, MediaPipe installed

---

### 2. Control Test (`control_test.py`)

Test finite state machine and controller.

```bash
python3 examples/control_test.py
```

**Features:**
- FSM state transitions
- Controller update loop
- Simulated vision data
- No hardware required

---

### 3. UART Test (`uart_test.py`)

Test UART communication with MCU.

```bash
python3 examples/uart_test.py
```

**Features:**
- MCU connection test
- Status reading
- Motor control commands
- Continuous status updates

**Requirements:**
- MCU connected and flashed
- Correct serial port

---

## Running Examples

Make sure you're in the Scouty root directory:

```bash
cd /path/to/Scouty
python3 examples/EXAMPLE_NAME.py
```

## Troubleshooting

### Import Errors

If you get import errors, make sure you're running from the Scouty root directory, or add it to PYTHONPATH:

```bash
export PYTHONPATH=/path/to/Scouty:$PYTHONPATH
python3 examples/vision_test.py
```

### Permission Errors (UART)

If you can't access serial ports:

```bash
sudo usermod -a -G dialout $USER
# Then logout and login again
```

### Camera Not Found

Try different camera IDs:

```python
camera = Camera(camera_id=0)  # Try 0, 1, 2, etc.
```

List available cameras:

```bash
v4l2-ctl --list-devices
```

## Creating Your Own Examples

Use these examples as templates for your own applications. Key patterns:

1. **Initialize components** in `__init__` or at start
2. **Open/connect** resources before use
3. **Close/disconnect** in finally blocks or context managers
4. **Handle errors** gracefully
5. **Add signal handlers** for clean shutdown

Example structure:

```python
def main():
    # Initialize
    component = Component()
    
    try:
        # Connect
        if not component.connect():
            return
        
        # Main loop
        while running:
            # Do work
            pass
    
    finally:
        # Cleanup
        component.close()
```

## Next Steps

After running the examples:
- Modify parameters to suit your robot
- Combine features for custom behaviors
- Add your own sensors and actuators
- Create integration tests
