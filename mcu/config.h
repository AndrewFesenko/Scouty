/**
 * Configuration file for MCU firmware
 * Pin assignments and system parameters
 */

#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// Pin definitions
#define MOTOR_A_PWM     5
#define MOTOR_A_DIR     4
#define MOTOR_B_PWM     6
#define MOTOR_B_DIR     7

#define ESTOP_PIN       2   // Emergency stop (interrupt capable)
#define VOLTAGE_PIN     A0  // Battery voltage monitor

// UART settings
#define UART_BAUD       115200
#define UART_BUFFER_SIZE 64

// Motor parameters
#define PWM_FREQUENCY   1000  // Hz
#define MAX_PWM_VALUE   255
#define MOTOR_DEADBAND  20    // Minimum PWM to overcome static friction

// Safety thresholds
#define MIN_BATTERY_VOLTAGE  10.5  // Volts (3S LiPo cutoff)
#define MAX_BATTERY_VOLTAGE  12.6  // Volts (3S LiPo full)
#define VOLTAGE_DIVIDER_RATIO 4.0  // Adjust based on voltage divider

// Command types (must match protocol.md)
#define CMD_SET_VELOCITY    0x01
#define CMD_STOP            0x02
#define CMD_RESET_ESTOP     0x03
#define CMD_GET_STATUS      0x04
#define STATUS_UPDATE       0x10

#endif // CONFIG_H
