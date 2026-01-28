/**
 * Safety monitoring implementation
 */

#include "safety.h"

void safety_init() {
    // Configure voltage monitoring pin
    pinMode(VOLTAGE_PIN, INPUT);
    
    // Emergency stop pin configured in main
}

bool safety_check() {
    // Check battery voltage
    float voltage = safety_get_battery_voltage();
    
    if (voltage < MIN_BATTERY_VOLTAGE) {
        return false;  // Battery too low
    }
    
    // Add more safety checks here:
    // - Temperature monitoring
    // - Current sensing
    // - Tilt detection
    
    return true;
}

uint8_t safety_get_battery_voltage() {
    // Read analog voltage
    int raw = analogRead(VOLTAGE_PIN);
    
    // Convert to voltage (assuming 10-bit ADC, 5V reference)
    float voltage = (raw / 1023.0) * 5.0 * VOLTAGE_DIVIDER_RATIO;
    
    // Scale to 0-255 for transmission
    uint8_t scaled = (uint8_t)((voltage / MAX_BATTERY_VOLTAGE) * 255);
    
    return scaled;
}
