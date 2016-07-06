# Updating the Kernel

It is highly recommended to update your kernel as part of your regular system updates instead of manually updating it.

The Raspberry Pi Foundation kernel is part of the `raspberrypi-bootloader` package. This package also contains the necessary bootloader files for the Broadcom chip.

You can also manually update the Rasperry Pi stock kernel, but this is not recommended. The `rpi-update` utility will download the latest version and copy all files into your system. Make sure it does not conflict with your distribution packages. It does not provide a way of automatically uninstalling the files.

You will have to reboot your Pi after upgrading the kernel to switch to the updated kernel.

If you are using a compiled kernel you will need to [rebuild](building.md) your kernel again.

Custom [configurations](configuring.md) can usually be copied over between minor kernel updates, but it's safer to use the diff utility to see what's changed and repeat your changes on the new configuration.
