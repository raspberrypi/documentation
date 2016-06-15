# Updating the Kernel

The Raspberry Pi Foundation kernel is part of the `raspberrypi-bootloader` package. This package also contains the necessary bootloader files for the Broadcom chip.

Your kernel will be updated automatically as part of your regular system updates.

Please do *not* use utilities like `rpi-update`. These are no longer maintained and will simply copy all files into your system without any backup and possible conflicts with your package manager. 

If you manually compiled your kernel, you will need to [rebuild](building.md) your kernel again.
Custom [configurations](configuring.md) can usually be copied over between minor kernel updates, but it's safer to use the diff utility to see what's changed and repeat your changes on the new configuration.

You will have to reboot your Pi after upgrading the kernel to switch to the updated kernel.
