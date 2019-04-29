
# BCM2837

The underlying architecture of the BCM2837 is identical to the BCM2836. The only significant difference is the replacement of the ARMv7 quad core cluster with a quad-core ARM Cortex A53 (ARMv8) cluster.

## Original variant - A0

This is the Broadcom chip used in the Raspberry Pi 3 and Raspberry Pi 2B version 1.2. The ARM cores  run at 1.2GHz, making the device about 50% faster than the Raspberry Pi 2. The VideoCore IV runs at 400MHz.

## New version - B0

The B0 variant runs the ARMs at 1.4GHz, making it around 17% faster than the A0.

The BCM2837B0 chip is packaged slightly differently to the BCM2837A0, and most notably includes a heat spreader for better thermals. These allow higher clock frequencies (or running at lower voltages to reduce power consumption), and more accurate monitoring and control of the chip's temperature.

[This post on the Raspberry Pi blog](https://www.raspberrypi.org/blog/raspberry-pi-3-model-bplus-sale-now-35/) goes into further detail about the BCM2837B0 chip.

Also see the Raspberry Pi 2's chip [BCM2836](../bcm2836/README.md) and the Raspberry Pi 1's chip [BCM2835](../bcm2835/README.md).
