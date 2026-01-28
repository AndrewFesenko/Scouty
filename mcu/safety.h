/**
 * Safety monitoring module
 * Battery voltage, emergency stop, etc.
 */

#ifndef SAFETY_H
#define SAFETY_H

#include "config.h"

void safety_init();
bool safety_check();
uint8_t safety_get_battery_voltage();

#endif // SAFETY_H
