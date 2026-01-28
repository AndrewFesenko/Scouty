"""
Simple example: UART communication test.
"""

from communication.uart_driver import UARTDriver
import time


def main():
    """Test UART communication with MCU."""
    print("Starting UART communication test...\n")
    
    # Initialize driver
    uart = UARTDriver(port='/dev/ttyUSB0', baudrate=115200)
    
    # Connect
    print("Connecting to MCU...")
    if not uart.connect():
        print("Error: Could not connect to MCU")
        print("Make sure:")
        print("  1. MCU is connected")
        print("  2. Correct port is specified")
        print("  3. You have permissions (sudo usermod -a -G dialout $USER)")
        return
    
    print("✓ Connected to MCU\n")
    
    try:
        # Test 1: Get status
        print("Test 1: Getting MCU status...")
        status = uart.get_status()
        if status:
            print(f"  Battery: {status['battery']}")
            print(f"  E-Stop: {status['estop']}")
            print(f"  Current L: {status['current_left']}")
            print(f"  Current R: {status['current_right']}")
        else:
            print("  No response from MCU")
        
        time.sleep(1)
        
        # Test 2: Set velocity
        print("\nTest 2: Setting motor velocities...")
        print("  Forward at 50% speed...")
        uart.set_velocity(125, 125)
        time.sleep(2)
        
        print("  Turning right...")
        uart.set_velocity(125, -125)
        time.sleep(2)
        
        print("  Turning left...")
        uart.set_velocity(-125, 125)
        time.sleep(2)
        
        print("  Stopping...")
        uart.stop()
        time.sleep(1)
        
        # Test 3: Read continuous status
        print("\nTest 3: Reading status updates (5 seconds)...")
        start_time = time.time()
        updates = 0
        
        while time.time() - start_time < 5:
            status = uart.read_status()
            if status:
                updates += 1
                print(f"  Update {updates}: Battery={status['battery']}, "
                      f"E-Stop={status['estop']}")
            time.sleep(0.1)
        
        print(f"\nReceived {updates} status updates")
        
    finally:
        # Stop and disconnect
        print("\nStopping motors and disconnecting...")
        uart.stop()
        uart.disconnect()
        print("✓ Test completed")


if __name__ == '__main__':
    main()
