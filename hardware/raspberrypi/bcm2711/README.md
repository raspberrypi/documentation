# BCM2711

This is the Broadcom chip used in the Raspberry Pi 4 Model B. The architecture of the BCM2711 is a considerable upgrade on that used by the SoCs in earlier Pi models. It continues the quad-core CPU design of the BCM2837, but uses the more powerful ARM A72 core. It has a greatly improved GPU feature set with much faster input/output, due to the incorporation of a PCIe link that connects the USB 2 and USB 3 ports, and a natively attached Ethernet controller. It is also capable of addressing more memory than the SoCs used before.

The ARM cores are capable of running at up to 1.5 GHz, making the Pi 4 about 50% faster than the Raspberry Pi 3B+. The new VideoCore VI 3D unit now runs at up to 500 MHz. The ARM cores are 64-bit, and while the VideoCore is 32-bit, there is a new Memory Management Unit, which means it can access more memory than previous versions.

The BCM2711 chip continues to use the heat spreading technology started with the BCM2837B0, which provides better thermal management. 

A datasheet for the BCM2711 can be found [here](https://datasheets.raspberrypi.org/bcm2711/bcm2711-peripherals.pdf).

## Some technical details

**Processor:**  Quad-core Cortex-A72 (ARM v8) 64-bit SoC @ 1.5 GHz. See [Wikipedia page](https://en.wikipedia.org/wiki/ARM_Cortex-A72) on the A72 for more details.

**Memory:** Accesses up to 4GB LPDDR4-2400 SDRAM (depending on model)

**Caches:** 32 KB data + 48 KB instruction L1 cache per core. 1MB L2 cache.

**Multimedia:** H.265 (4Kp60 decode); H.264 (1080p60 decode, 1080p30 encode); OpenGL ES, 3.0 graphics

**I/O:** PCIe bus, onboard Ethernet port, 2 × DSI ports (only one exposed on Raspberry Pi 4B), 2 × CSI ports (only one exposed on Raspberry Pi 4B), up to 6 × I2C, up to 6 × UART (muxed with I2C), up to 6 × SPI (only five exposed on Raspberry Pi 4B), dual HDMI video output, composite video output.


See the following documentation sections for information about the previous Raspberry Pi chips:

* Raspberry Pi 3+ chip [BCM2837B0](../bcm2837b0/README.md)
* Raspberry Pi 3 chip [BCM2837](../bcm2837/README.md)
* Raspberry Pi 2 chip [BCM2836](../bcm2836/README.md)
* Raspberry Pi 1 chip [BCM2835](../bcm2835/README.md)
