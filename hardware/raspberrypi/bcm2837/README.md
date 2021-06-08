# BCM2837

This is the Broadcom chip used in the Raspberry Pi 3, and in later models of the Raspberry Pi 2. The underlying architecture of the BCM2837 is identical to the BCM2836. The only significant difference is the replacement of the ARMv7 quad core cluster with a quad-core ARM Cortex A53 (ARMv8) cluster.

The ARM cores run at 1.2GHz, making the device about 50% faster than the Raspberry Pi 2. The VideoCore IV runs at 400MHz.

Please refer to the following BCM2836 document for details on the ARM peripherals specification, which also applies to the BCM2837.

- [BCM2836 ARM-local peripherals](../bcm2836/QA7_rev3.4.pdf)
- [Cortex-A53 MPCore Processor Technical Reference Manual](https://developer.arm.com/documentation/ddi0500/latest/)

Also see the Raspberry Pi 2's chip [BCM2836](../bcm2836/README.md) and the Raspberry Pi 1's chip [BCM2835](../bcm2835/README.md).
