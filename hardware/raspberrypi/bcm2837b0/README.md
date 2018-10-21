# BCM2837B0

This is the Broadcom chip used in the Raspberry Pi 3B+. The underlying architecture of the BCM2837B0 is identical to the BCM2836 and BCM2837. The only significant difference is the replacement of the ARMv7 quad core cluster with a quad-core ARM Cortex A53 (ARMv8) cluster.

The ARM cores run at 1.4GHz, making the device about 17% faster than the original Raspberry Pi 3. The VideoCore IV runs at 400MHz.

Regarding the BCM2837B0 chip itself, it is an updated version of the 64-bit Broadcom application processor used in Raspberry Pi 3B, which incorporates power integrity optimisations, and a heat spreader. These allow higher clock frequencies (or to run at lower voltages to reduce power consumption), and to more accurately monitor and control the temperature of
the chip.

This [blog post](https://www.raspberrypi.org/blog/raspberry-pi-3-model-bplus-sale-now-35/) on the official Raspberry Pi foundation website goes into further detail about the BCM2837B0 chip.

Also see the following documents for information about the previous Raspberry Pi chips:

* Raspberry Pi 3 chip [BCM2837](../bcm2837/README.md)
* Raspberry Pi 2 chip [BCM2836](../bcm2836/README.md)
* Raspberry Pi 1 chip [BCM2835](../bcm2835/README.md)
