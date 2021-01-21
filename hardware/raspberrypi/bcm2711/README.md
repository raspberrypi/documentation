# BCM2711

Used on the Raspberry Pi 4B, 400 and Compute Module 4.

The architecture of the BCM2711 is a considerable upgrade on that used by the SoCs in earlier Pi models. It continues the quad-core CPU design of the BCM2837, but uses the more powerful ARM A72 core. It has a greatly improved GPU feature set with much faster input/output, due to the incorporation of a PCIe link that connects the USB 2 and USB 3 ports, and a natively attached Ethernet controller. It is also capable of addressing more memory than the SoCs used before.

The ARM cores are clocked at 1.5GHz on the Pi 4B and 1.8GHz on the Pi 400. The new VideoCore VI 3D unit runs at up to 550 MHz. The ARM cores are 64-bit, and while the VideoCore is 32-bit, it has its own MMU, which allows it to access more memory than previous SoCs.

The BCM2711 chip continues to use the heat spreading technology started with the BCM2837B0, which provides better thermal management. 

- [BCM2711 Datasheet](https://datasheets.raspberrypi.org/bcm2711/bcm2711-peripherals.pdf)
