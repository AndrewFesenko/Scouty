/**
 * UART communication module
 * Protocol implementation for Raspberry Pi communication
 */

#ifndef UART_COMM_H
#define UART_COMM_H

#include "config.h"

void uart_init();
bool uart_available();
int uart_read_packet(uint8_t* buffer, int max_length);
void uart_write_packet(uint8_t* buffer, int length);

#endif // UART_COMM_H
