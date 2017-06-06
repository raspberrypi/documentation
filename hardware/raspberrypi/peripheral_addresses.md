# Peripheral Addresses

If there is no kernel driver available, and a program needs to access a peripheral address directly with mmap, it needs to know where in the virtual memory map the peripheral bus segment has been placed. This varies according to which model of Raspberry Pi is being used, so there are three helper function available to provide platform independence. **Note**: please use these functions rather than hardcoded values, as this will ensure future compatibility.

`unsigned bcm_host_get_peripheral_address()`

This returns the ARM-side physical address where peripherals are mapped. This is 0x20000000 on the Pi Zero, Pi Zero W, and the first generation of the Raspberry Pi and Compute Module, and 0x3f000000 on the Pi 2, Pi 3 and Compute Module 3.

`unsigned bcm_host_get_peripheral_size()`

This returns the size of the peripheral's space, which is 0x01000000 for all models.

`unsigned bcm_host_get_sdram_address()`

This returns the bus address of the SDRAM. This is 0x40000000 on the Pi Zero, Pi Zero W, and the first generation of the Raspberry Pi and Compute Module (GPU L2 cached), and 0xC0000000 on the Pi 2, Pi 3 and Compute Module 3 (uncached).
