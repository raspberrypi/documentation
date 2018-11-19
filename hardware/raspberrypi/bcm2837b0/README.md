# BCM2837B0

This is the Broadcom chip used in the Raspberry Pi 3B+. The underlying architecture of the BCM2837B0 is identical to the BCM2837A0 chip used in other versions of the Pi. The ARM core hardware is the same, only the frequency is rated higher.

 The ARM cores are capable of running up to 1.4GHz, making the device about 17% faster than the original Raspberry Pi 3. The VideoCore IV runs at 400MHz. The ARM core is 64-bit while the VideoCore IV is 32-bit.

Regarding the BCM2837B0 chip itself, it is packaged slightly differently than the BCM2837A0 and most notably includes a heat spreader for better thermals. These allow higher clock frequencies (or to run at lower voltages to reduce power consumption), and to more accurately monitor and control the temperature of the chip.

This [blog post](https://www.raspberrypi.org/blog/raspberry-pi-3-model-bplus-sale-now-35/) on the official Raspberry Pi foundation website goes into further detail about the BCM2837B0 chip.

Also see the following documents for information about the previous Raspberry Pi chips:

* Raspberry Pi 3 chip [BCM2837](../bcm2837/README.md)
* Raspberry Pi 2 chip [BCM2836](../bcm2836/README.md)
* Raspberry Pi 1 chip [BCM2835](../bcm2835/README.md)
