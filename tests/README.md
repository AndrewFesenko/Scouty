# Testing

Test suite for Scouty robot components.

## Test Organization

- `test_vision.py` - Vision system tests
- `test_control.py` - Control system and FSM tests
- `test_communication.py` - UART protocol tests
- `integration/` - Integration tests
- `hardware/` - Hardware-in-the-loop tests

## Running Tests

### Python Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run specific test file
pytest tests/test_vision.py

# Run with coverage
pytest --cov=vision --cov=control --cov=communication
```

### Hardware Tests

Hardware tests require actual hardware connected.

```bash
# Run hardware tests (requires --hardware flag)
pytest tests/hardware/ --hardware
```

## Test Coverage Goals

- Vision: >80%
- Control: >90%
- Communication: >85%

## Continuous Integration

Tests are automatically run on:
- Pull requests
- Commits to main branch

## Writing Tests

Follow pytest conventions:
- Test files start with `test_`
- Test functions start with `test_`
- Use fixtures for setup/teardown
- Mock hardware dependencies when possible
