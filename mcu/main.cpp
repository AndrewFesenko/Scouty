/**
 * Main firmware for Scouty robot motor controller
 * 
 * Handles:
 * - Motor control (PWM)
 * - UART communication with Raspberry Pi
 * - Safety monitoring
 * - Emergency stop
 */

#include "config.h"
#include "motor_control.h"
#include "uart_comm.h"
#include "safety.h"

// Global state
volatile bool emergency_stop = false;
volatile uint32_t last_command_time = 0;

// Watchdog timeout (ms)
#define WATCHDOG_TIMEOUT 1000

void setup() {
    // Initialize serial communication
    uart_init();
    
    // Initialize motor control
    motor_init();
    
    // Initialize safety systems
    safety_init();
    
    // Setup emergency stop interrupt
    pinMode(ESTOP_PIN, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(ESTOP_PIN), estop_isr, FALLING);
    
    // Initial state - motors stopped
    motor_stop_all();
    
    last_command_time = millis();
}

void loop() {
    // Check for emergency stop
    if (emergency_stop) {
        motor_stop_all();
        delay(100);
        return;
    }
    
    // Check watchdog timeout
    if (millis() - last_command_time > WATCHDOG_TIMEOUT) {
        motor_stop_all();
        // Continue running but don't execute commands
    }
    
    // Check safety systems
    if (!safety_check()) {
        motor_stop_all();
        emergency_stop = true;
        return;
    }
    
    // Process incoming UART commands
    if (uart_available()) {
        uint8_t cmd_buffer[UART_BUFFER_SIZE];
        int len = uart_read_packet(cmd_buffer, UART_BUFFER_SIZE);
        
        if (len > 0) {
            process_command(cmd_buffer, len);
            last_command_time = millis();
        }
    }
    
    // Send status update periodically
    static uint32_t last_status_time = 0;
    if (millis() - last_status_time > 100) {  // 10Hz status updates
        send_status();
        last_status_time = millis();
    }
    
    delay(10);  // 100Hz loop rate
}

void process_command(uint8_t* buffer, int length) {
    if (length < 3) return;  // Minimum packet size
    
    uint8_t cmd_type = buffer[0];
    
    switch (cmd_type) {
        case CMD_SET_VELOCITY: {
            if (length >= 5) {
                int16_t left_vel = (buffer[1] << 8) | buffer[2];
                int16_t right_vel = (buffer[3] << 8) | buffer[4];
                motor_set_velocity(left_vel, right_vel);
            }
            break;
        }
        
        case CMD_STOP: {
            motor_stop_all();
            break;
        }
        
        case CMD_RESET_ESTOP: {
            if (!digitalRead(ESTOP_PIN)) {  // Check if button still pressed
                emergency_stop = false;
            }
            break;
        }
        
        case CMD_GET_STATUS: {
            send_status();
            break;
        }
        
        default:
            // Unknown command
            break;
    }
}

void send_status() {
    uint8_t status_buffer[16];
    status_buffer[0] = STATUS_UPDATE;
    
    // Battery voltage (scaled to 0-255)
    status_buffer[1] = safety_get_battery_voltage();
    
    // Emergency stop status
    status_buffer[2] = emergency_stop ? 1 : 0;
    
    // Motor current (if available)
    status_buffer[3] = 0;  // Placeholder
    status_buffer[4] = 0;
    
    uart_write_packet(status_buffer, 5);
}

void estop_isr() {
    // Emergency stop interrupt handler
    emergency_stop = true;
    motor_stop_all();
}
