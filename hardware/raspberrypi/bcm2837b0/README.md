# BCM2837B0

This is the Broadcom chip used in the Raspberry Pi 3B+ and 3A+. The underlying architecture of the BCM2837B0 is identical to the BCM2837A0 chip used in other versions of the Pi. The ARM core hardware is the same, only the frequency is rated higher.

The ARM cores are capable of running at up to 1.4GHz, making the 3B+/3A+ about 17% faster than the original Raspberry Pi 3. The VideoCore IV runs at 400MHz. The ARM core is 64-bit, while the VideoCore IV is 32-bit.

The BCM2837B0 chip is packaged slightly differently to the BCM2837A0, and most notably includes a heat spreader for better thermals. These allow higher clock frequencies (or running at lower voltages to reduce power consumption), and more accurate monitoring and control of the chip's temperature.

[This post on the Raspberry Pi blog](https://www.raspberrypi.org/blog/raspberry-pi-3-model-bplus-sale-now-35/) goes into further detail about the BCM2837B0 chip.

Also see the following documents for information about the previous Raspberry Pi chips:

* Raspberry Pi 3 chip [BCM2837](../bcm2837/README.md)
* Raspberry Pi 2 chip [BCM2836](../bcm2836/README.md)
* Raspberry Pi 1 chip [BCM2835](../bcm2835/README.md)
