# Peripheral Addresses

If there is no kernel driver available, and a program needs to access a peripheral addresses directly with mmap, it needs to know where in the virtual memory map the peripheral bus segment has been placed. This varies according to the model of Raspberry Pi being used, so there are three helper function available to provide platform independence. Please use these functions rather than hardcoded values as this will ensure future compatibility.


`unsigned bcm_host_get_peripheral_address()`

Returns the ARM side physical address of where peripherals are mapped, 0x20000000 on Pi1/Pi0/Pi0W/CM and 0x3f000000 on Pi2/Pi3/CM3

`unsigned bcm_host_get_peripheral_size()`

Returns the size of the peripherals space, 0x01000000 for all models.

`unsigned bcm_host_get_sdram_address()`

Returns the bus address of the SDRAM, 0x40000000 on Pi1/Pi0/Pi0W/CM (GPU L2 cached) and 0xC0000000 on Pi2/Pi3/CM3 (uncached).
