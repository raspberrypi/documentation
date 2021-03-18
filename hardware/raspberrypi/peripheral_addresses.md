# Peripheral Addresses

If there is no kernel driver available, and a program needs to access a peripheral address directly with mmap, it needs to know where in the virtual memory map the peripheral bus segment has been placed. This varies according to which model of Raspberry Pi is being used, so there are three helper function available to provide platform independence. **Note**: please use these functions rather than hardcoded values, as this will ensure future compatibility.

`unsigned bcm_host_get_peripheral_address()`

This returns the ARM-side physical address where peripherals are mapped. Values are as follows:

| SoC | Peripheral Address | Source |
| --- | --- | --- |
| BCM2835 | 0x20000000 | [bcm2835.dtsi](https://github.com/raspberrypi/linux/blob/7f465f823c2ecbade5877b8bbcb2093a8060cb0e/arch/arm/boot/dts/bcm2835.dtsi#L21) |
| BCM2836 | 0x3f000000 | [bcm2836.dtsi](https://github.com/raspberrypi/linux/blob/7f465f823c2ecbade5877b8bbcb2093a8060cb0e/arch/arm/boot/dts/bcm2836.dtsi#L10) |
| BCM2837 | 0x3f000000 | [bcm2837.dtsi](https://github.com/raspberrypi/linux/blob/7f465f823c2ecbade5877b8bbcb2093a8060cb0e/arch/arm/boot/dts/bcm2837.dtsi#L9) |
| BCM2711 | 0xfe000000 | [bcm2711.dtsi](https://github.com/raspberrypi/linux/blob/7f465f823c2ecbade5877b8bbcb2093a8060cb0e/arch/arm/boot/dts/bcm2711.dtsi#L41) |

`unsigned bcm_host_get_peripheral_size()`

This returns the size of the peripheral's space, which is 0x01000000 for all models.

`unsigned bcm_host_get_sdram_address()`

This returns the bus address of the SDRAM. This is 0x40000000 on the Pi Zero, Pi Zero W, and the first generation of the Raspberry Pi and Compute Module (GPU L2 cached), and 0xC0000000 on the Pi 2, Pi 3 and Compute Module 3 (uncached).

## Building a C program using these functions

The `include` file and library are installed by default on a Raspberry Pi OS system.

Add the following line to your C program:
```
#include <bcm_host.h>
```
Link with:
```
-lbcm_host
```
So a simple command line compile might be:
```
cc myfile.c -I/opt/vc/include -L/opt/vc/lib -lbcm_host -o myfile
```
