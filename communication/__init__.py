"""
Communication module for Scouty robot.
UART protocol implementation.
"""

__version__ = "0.1.0"

from .uart_driver import UARTDriver

__all__ = ['UARTDriver']
