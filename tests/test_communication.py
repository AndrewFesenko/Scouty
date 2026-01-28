"""
Tests for communication module.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from communication.uart_driver import UARTDriver


class TestUARTDriver:
    """Tests for UART Driver."""
    
    def test_initialization(self):
        """Test UART driver initialization."""
        driver = UARTDriver(port='/dev/ttyUSB0', baudrate=115200)
        assert driver.port == '/dev/ttyUSB0'
        assert driver.baudrate == 115200
        assert not driver.is_connected
    
    def test_checksum_calculation(self):
        """Test checksum calculation."""
        driver = UARTDriver()
        data = bytes([0x01, 0x02, 0x03])
        checksum = driver._calculate_checksum(data)
        assert checksum == 6
    
    @patch('serial.Serial')
    def test_connect(self, mock_serial):
        """Test connection."""
        mock_serial_instance = Mock()
        mock_serial.return_value = mock_serial_instance
        
        driver = UARTDriver()
        result = driver.connect()
        
        assert result is True
        assert driver.is_connected
    
    @patch('serial.Serial')
    def test_disconnect(self, mock_serial):
        """Test disconnection."""
        mock_serial_instance = Mock()
        mock_serial_instance.is_open = True
        mock_serial.return_value = mock_serial_instance
        
        driver = UARTDriver()
        driver.connect()
        driver.disconnect()
        
        assert not driver.is_connected
    
    @patch('serial.Serial')
    def test_set_velocity(self, mock_serial):
        """Test set velocity command."""
        mock_serial_instance = Mock()
        mock_serial_instance.write = Mock(return_value=None)
        mock_serial.return_value = mock_serial_instance
        
        driver = UARTDriver()
        driver.connect()
        result = driver.set_velocity(100, -50)
        
        assert result is True
        assert mock_serial_instance.write.called
    
    @patch('serial.Serial')
    def test_stop(self, mock_serial):
        """Test stop command."""
        mock_serial_instance = Mock()
        mock_serial_instance.write = Mock(return_value=None)
        mock_serial.return_value = mock_serial_instance
        
        driver = UARTDriver()
        driver.connect()
        result = driver.stop()
        
        assert result is True
        assert mock_serial_instance.write.called


if __name__ == '__main__':
    pytest.main([__file__])
