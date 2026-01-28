/**
 * Motor control module
 * PWM generation and motor driver interface
 */

#ifndef MOTOR_CONTROL_H
#define MOTOR_CONTROL_H

#include "config.h"

void motor_init();
void motor_set_velocity(int16_t left_vel, int16_t right_vel);
void motor_stop_all();

#endif // MOTOR_CONTROL_H
