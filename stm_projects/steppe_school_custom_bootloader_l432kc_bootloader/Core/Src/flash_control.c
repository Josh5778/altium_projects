#include "flash_control.h"
#include "stdint.h"
#include "main.h"

void erase_flash_memory()
{
	FLASH_EraseInitTypeDef flash_erase_struct = {0};
	uint32_t  error_status = 0;
	HAL_FLASH_Unlock();
	// defining the members of a struct
	flash_erase_struct.TypeErase = FLASH_TYPEERASE_PAGES;
	// defining an onset number page to be erased
	flash_erase_struct.Page = (APPLICATION_ADDRESS - FLASH_BASE) / FLASH_PAGE_SIZE;
	// number of pages to remove
	flash_erase_struct.NbPages = (FLASH_BANK1_END + 1UL - APPLICATION_ADDRESS)/ FLASH_PAGE_SIZE;
	// First Bank 1
	flash_erase_struct.Banks = FLASH_BANK_1;

	// erase the pages, this step is mandatory
    HAL_StatusTypeDef status = HAL_FLASHEx_Erase(&flash_erase_struct, &error_status);

	HAL_FLASH_Lock();
}

void store_flash_memory(uint32_t memory_address, uint8_t *data, uint16_t data_length)
{
	uint8_t data_temp[8];
	HAL_FLASH_Unlock();
	int pointer_element = 0;
	// erase the flash memory if written for the first time
	if(memory_address == APPLICATION_ADDRESS)
	{
		erase_flash_memory();
		HAL_FLASH_Unlock();
	}
	// using while loop, convey all data to the flash memory
	while (data_length > 8)
	{
		HAL_FLASH_Program(FLASH_TYPEPROGRAM_DOUBLEWORD, memory_address + pointer_element,
											*((uint64_t *)&data[pointer_element]));
		pointer_element += 8;
		data_length -= 8;
	}
	if(data_length > 0)
	{
		for(int i = 0 ; i < data_length ; i ++)
		{
			data_temp[i] = data[pointer_element + i];
		}
		HAL_FLASH_Program(FLASH_TYPEPROGRAM_DOUBLEWORD, memory_address + pointer_element,
													*((uint64_t *)data_temp));
	}
	// lock the memory
	HAL_FLASH_Lock();
}

void run_application()
{

}
