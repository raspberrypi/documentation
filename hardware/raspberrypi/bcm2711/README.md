# BCM2711

This is the Broadcom chip used in the Raspberry Pi 4B. The architecture of the BCM2711 is a considerable upgrade on that used by the SoC's in the previous models of the Pi. It continues with the 4 core design of the 2837, but using the more powerful ARM A72 core. It has a greatly improved GPU feature set, with much faster I/O with the incorporation of a PCIe databus which connects the USB 2 and USB ports, and a natively attached ethernet controller. It is also capable of adddressing more memory than the SoC's used up until now.

The ARM cores are capable of running at up to 1.5GHz, making the Pi4 about 50% faster than the Raspberry Pi 3+. The new VideoCore V 3D unit now runs at up to 500MHz. The ARM cores are 64-bit, and while the VideoCore V is 32-bit it now addresses through a new Memory Management Unit which means it can access more memory.

The BCM2711 chip continues to use the heat spreading model started with the BCM2837B0, to provide better thermal management. 


## Some Technical Details

**Processor:**  Quad-core Cortex-A72 (ARM v8) 64-bit SoC @ 1.5GHz

**Memory:** Accesses up to 4GB LPDDR4-2400 SDRAM (depending on model)

**Multimedia:** H.265 (4Kp60 decode); H.264 (1080p60 decode, 1080p30 encode); OpenGL ES, 3.0 graphics

**I/O:** PCIe bus, on board ethernet, 2xDSI ports (only one exposed on Raspberry Pi 4B), 2xCSI ports (only one exposed on Raspberry Pi 4B), up to 4xI2C, up to 4xUART (muxed with I2C).

Also see the following documents for information about the previous Raspberry Pi chips:

* Raspberry Pi 3+ chip [BCM2837B0](../bcm2837bO/README.md)
* Raspberry Pi 3 chip [BCM2837](../bcm2837/README.md)
* Raspberry Pi 2 chip [BCM2836](../bcm2836/README.md)
* Raspberry Pi 1 chip [BCM2835](../bcm2835/README.md)
