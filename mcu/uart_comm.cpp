/**
 * UART communication implementation
 */

#include "uart_comm.h"

// Packet structure: [START_BYTE][LENGTH][DATA...][CHECKSUM]
#define START_BYTE 0xAA

void uart_init() {
    Serial.begin(UART_BAUD);
    while (!Serial && millis() < 3000) {
        // Wait for serial to initialize (max 3 seconds)
    }
}

bool uart_available() {
    return Serial.available() > 0;
}

int uart_read_packet(uint8_t* buffer, int max_length) {
    // Wait for start byte
    if (!Serial.available()) return 0;
    
    uint8_t byte = Serial.read();
    if (byte != START_BYTE) return 0;
    
    // Read length
    while (!Serial.available());
    uint8_t length = Serial.read();
    
    if (length == 0 || length > max_length) return 0;
    
    // Read data
    int bytes_read = 0;
    uint32_t timeout = millis() + 100;
    
    while (bytes_read < length && millis() < timeout) {
        if (Serial.available()) {
            buffer[bytes_read++] = Serial.read();
        }
    }
    
    if (bytes_read != length) return 0;
    
    // Read checksum
    while (!Serial.available() && millis() < timeout);
    if (!Serial.available()) return 0;
    
    uint8_t checksum = Serial.read();
    
    // Verify checksum (simple sum)
    uint8_t calc_checksum = 0;
    for (int i = 0; i < length; i++) {
        calc_checksum += buffer[i];
    }
    
    if (checksum != calc_checksum) return 0;
    
    return length;
}

void uart_write_packet(uint8_t* buffer, int length) {
    if (length == 0 || length > 255) return;
    
    // Send start byte
    Serial.write(START_BYTE);
    
    // Send length
    Serial.write((uint8_t)length);
    
    // Send data
    Serial.write(buffer, length);
    
    // Calculate and send checksum
    uint8_t checksum = 0;
    for (int i = 0; i < length; i++) {
        checksum += buffer[i];
    }
    Serial.write(checksum);
}
