# Contributing to Scouty

First off, thank you for considering contributing to Scouty! It's people like you that make Scouty such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by a code of conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples
- Describe the behavior you observed and what you expected
- Include logs, error messages, and screenshots if applicable
- Note your environment (OS, Python version, hardware)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- Use a clear and descriptive title
- Provide a detailed description of the proposed functionality
- Explain why this enhancement would be useful
- List any similar features in other projects (if applicable)

### Pull Requests

1. Fork the repository and create your branch from `main`
2. If you've added code, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows the existing style
6. Write a clear commit message

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Scouty.git
cd Scouty

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -r vision/requirements.txt
pip install -r communication/requirements.txt
pip install -r tests/requirements.txt
```

## Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions focused and small
- Comment complex logic

### Python Style Example

```python
def calculate_distance(point1: Tuple[float, float], 
                      point2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Args:
        point1: First point (x, y)
        point2: Second point (x, y)
        
    Returns:
        Distance between points
    """
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return math.sqrt(dx**2 + dy**2)
```

### C++ Style (for MCU firmware)

- Follow Arduino style guide
- Use meaningful variable names
- Add comments for hardware-specific code
- Document pin assignments

## Testing

- Write tests for new features
- Maintain or improve code coverage
- Run the full test suite before submitting PR

```bash
pytest tests/
pytest --cov=vision --cov=control --cov=communication
```

## Documentation

- Update README.md if you change functionality
- Update relevant documentation in `docs/`
- Add docstrings to new functions and classes
- Include code examples for new features

## Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters
- Reference issues and pull requests liberally

### Good Commit Messages

```
Add person detection timeout parameter

- Add configurable timeout for person detection
- Update tests to cover timeout behavior
- Document new parameter in API reference

Fixes #123
```

## Project Structure

When adding new features:

- Vision code goes in `vision/`
- Control logic goes in `control/`
- Communication code goes in `communication/`
- MCU firmware goes in `mcu/`
- Tests go in `tests/`
- Documentation goes in `docs/`

## Questions?

Feel free to open an issue with your question or contact the maintainers directly.

Thank you for contributing to Scouty! 🤖
