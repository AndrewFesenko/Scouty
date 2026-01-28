"""
UART driver for communication with microcontroller.
Implements the protocol specified in protocol.md
"""

import serial
import struct
import time
from typing import Optional, Dict, Tuple


class UARTDriver:
    """
    UART driver for Raspberry Pi to MCU communication.
    """
    
    # Protocol constants
    START_BYTE = 0xAA
    
    # Command types
    CMD_SET_VELOCITY = 0x01
    CMD_STOP = 0x02
    CMD_RESET_ESTOP = 0x03
    CMD_GET_STATUS = 0x04
    STATUS_UPDATE = 0x10
    
    def __init__(self, port: str = '/dev/ttyUSB0', baudrate: int = 115200, 
                 timeout: float = 0.1):
        """
        Initialize UART driver.
        
        Args:
            port: Serial port device (e.g., '/dev/ttyUSB0')
            baudrate: Communication baud rate
            timeout: Read timeout in seconds
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None
        self.is_connected = False
        
    def connect(self) -> bool:
        """
        Open serial connection.
        
        Returns:
            True if connection successful
        """
        try:
            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=self.timeout
            )
            self.is_connected = True
            time.sleep(0.1)  # Allow time for connection to stabilize
            return True
        except serial.SerialException as e:
            print(f"Failed to connect: {e}")
            return False
    
    def disconnect(self):
        """Close serial connection."""
        if self.serial and self.serial.is_open:
            self.serial.close()
        self.is_connected = False
    
    def _calculate_checksum(self, data: bytes) -> int:
        """
        Calculate checksum for data.
        
        Args:
            data: Data bytes
            
        Returns:
            Checksum value (0-255)
        """
        return sum(data) & 0xFF
    
    def _send_packet(self, data: bytes) -> bool:
        """
        Send packet with protocol framing.
        
        Args:
            data: Data payload
            
        Returns:
            True if sent successfully
        """
        if not self.is_connected or not self.serial:
            return False
        
        length = len(data)
        if length == 0 or length > 255:
            return False
        
        # Build packet
        packet = bytes([self.START_BYTE, length]) + data
        checksum = self._calculate_checksum(data)
        packet += bytes([checksum])
        
        try:
            self.serial.write(packet)
            return True
        except serial.SerialException:
            return False
    
    def _receive_packet(self, timeout: float = 1.0) -> Optional[bytes]:
        """
        Receive packet with protocol framing.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Data payload or None if error/timeout
        """
        if not self.is_connected or not self.serial:
            return None
        
        start_time = time.time()
        
        # Wait for start byte
        while time.time() - start_time < timeout:
            if self.serial.in_waiting > 0:
                byte = self.serial.read(1)
                if byte[0] == self.START_BYTE:
                    break
        else:
            return None  # Timeout
        
        # Read length
        length_byte = self.serial.read(1)
        if len(length_byte) == 0:
            return None
        
        length = length_byte[0]
        if length == 0:
            return None
        
        # Read data
        data = self.serial.read(length)
        if len(data) != length:
            return None
        
        # Read checksum
        checksum_byte = self.serial.read(1)
        if len(checksum_byte) == 0:
            return None
        
        # Verify checksum
        expected_checksum = self._calculate_checksum(data)
        if checksum_byte[0] != expected_checksum:
            return None
        
        return data
    
    def set_velocity(self, left_vel: int, right_vel: int) -> bool:
        """
        Set motor velocities.
        
        Args:
            left_vel: Left motor velocity (-255 to +255)
            right_vel: Right motor velocity (-255 to +255)
            
        Returns:
            True if command sent successfully
        """
        # Clamp values
        left_vel = max(-255, min(255, left_vel))
        right_vel = max(-255, min(255, right_vel))
        
        # Pack command
        data = struct.pack('>Bhh', self.CMD_SET_VELOCITY, left_vel, right_vel)
        
        return self._send_packet(data)
    
    def stop(self) -> bool:
        """
        Stop all motors.
        
        Returns:
            True if command sent successfully
        """
        data = bytes([self.CMD_STOP])
        return self._send_packet(data)
    
    def reset_estop(self) -> bool:
        """
        Reset emergency stop.
        
        Returns:
            True if command sent successfully
        """
        data = bytes([self.CMD_RESET_ESTOP])
        return self._send_packet(data)
    
    def get_status(self, timeout: float = 0.5) -> Optional[Dict]:
        """
        Request and receive status from MCU.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            Status dictionary or None
        """
        # Send request
        data = bytes([self.CMD_GET_STATUS])
        if not self._send_packet(data):
            return None
        
        # Receive response
        response = self._receive_packet(timeout)
        
        if response and len(response) >= 5 and response[0] == self.STATUS_UPDATE:
            return {
                'battery': response[1],
                'estop': response[2] != 0,
                'current_left': response[3],
                'current_right': response[4]
            }
        
        return None
    
    def read_status(self) -> Optional[Dict]:
        """
        Read status update if available (non-blocking).
        
        Returns:
            Status dictionary or None
        """
        if not self.is_connected or not self.serial:
            return None
        
        if self.serial.in_waiting == 0:
            return None
        
        response = self._receive_packet(timeout=0.1)
        
        if response and len(response) >= 5 and response[0] == self.STATUS_UPDATE:
            return {
                'battery': response[1],
                'estop': response[2] != 0,
                'current_left': response[3],
                'current_right': response[4]
            }
        
        return None
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
