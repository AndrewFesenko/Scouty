/**
 * Motor control implementation
 */

#include "motor_control.h"

void motor_init() {
    // Configure motor pins as outputs
    pinMode(MOTOR_A_PWM, OUTPUT);
    pinMode(MOTOR_A_DIR, OUTPUT);
    pinMode(MOTOR_B_PWM, OUTPUT);
    pinMode(MOTOR_B_DIR, OUTPUT);
    
    // Set PWM frequency (if supported by platform)
    #ifdef ESP32
    ledcSetup(0, PWM_FREQUENCY, 8);  // Channel 0, 8-bit resolution
    ledcSetup(1, PWM_FREQUENCY, 8);  // Channel 1
    ledcAttachPin(MOTOR_A_PWM, 0);
    ledcAttachPin(MOTOR_B_PWM, 1);
    #endif
    
    // Initialize with motors stopped
    motor_stop_all();
}

void motor_set_velocity(int16_t left_vel, int16_t right_vel) {
    // left_vel and right_vel range: -255 to +255
    
    // Motor A (left)
    if (left_vel > 0) {
        digitalWrite(MOTOR_A_DIR, HIGH);
        int pwm = constrain(left_vel, 0, MAX_PWM_VALUE);
        if (pwm < MOTOR_DEADBAND) pwm = 0;
        analogWrite(MOTOR_A_PWM, pwm);
    } else if (left_vel < 0) {
        digitalWrite(MOTOR_A_DIR, LOW);
        int pwm = constrain(-left_vel, 0, MAX_PWM_VALUE);
        if (pwm < MOTOR_DEADBAND) pwm = 0;
        analogWrite(MOTOR_A_PWM, pwm);
    } else {
        analogWrite(MOTOR_A_PWM, 0);
    }
    
    // Motor B (right)
    if (right_vel > 0) {
        digitalWrite(MOTOR_B_DIR, HIGH);
        int pwm = constrain(right_vel, 0, MAX_PWM_VALUE);
        if (pwm < MOTOR_DEADBAND) pwm = 0;
        analogWrite(MOTOR_B_PWM, pwm);
    } else if (right_vel < 0) {
        digitalWrite(MOTOR_B_DIR, LOW);
        int pwm = constrain(-right_vel, 0, MAX_PWM_VALUE);
        if (pwm < MOTOR_DEADBAND) pwm = 0;
        analogWrite(MOTOR_B_PWM, pwm);
    } else {
        analogWrite(MOTOR_B_PWM, 0);
    }
}

void motor_stop_all() {
    analogWrite(MOTOR_A_PWM, 0);
    analogWrite(MOTOR_B_PWM, 0);
}
