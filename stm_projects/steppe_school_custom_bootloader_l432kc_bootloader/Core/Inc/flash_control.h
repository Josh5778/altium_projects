#ifndef INC_FLASH_CONTROL_H_
#define INC_FLASH_CONTROL_H_

#include "stdio.h"
#include "main.h"

#define APPLICATION_ADDRESS 0x8008000UL

void store_flash_memory(uint32_t memory_address, uint8_t *data, uint16_t data_length);
void erase_flash_memory();
#endif /* INC_FLASH_CONTROL_H_ */
