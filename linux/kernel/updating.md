# Updating the kernel

It is highly recommended that you update your kernel as part of your regular system updates, instead of manually updating it.

The Raspberry Pi Foundation kernel is part of the `raspberrypi-bootloader` package. This package also contains the necessary bootloader files for the Broadcom chip.

You can also manually update the Rasperry Pi stock kernel, but this is not recommended. The `rpi-update` utility will download the latest version and copy all files into your system. Make sure it doesn't conflict with your distribution packages. It doesn't provide a way of automatically uninstalling the files.

After upgrading the kernel, you'll have to reboot your Pi to switch to the updated version.

If you're using a compiled kernel, you'll need to [rebuild](building.md) your kernel again.

Custom [configurations](configuring.md) can usually be copied over between minor kernel updates, but it's safer to use the `diff` utility to see what's changed and repeat your changes on the new configuration.

To revert to the current stock Raspbian kernel after trying `rpi-update` or a custom kernel, run:
```
sudo apt-get install --reinstall raspberrypi-bootloader
```
