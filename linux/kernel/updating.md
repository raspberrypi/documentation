# Updating the kernel

If you use the standard Raspbian update/upgrade process (found [here](../../raspbian/updating.md)), this will automatically update the kernel to the latest stable version. This is the recommended procedure. However, in certain circumstances, you may wish to update to the latest 'bleeding edge' or test kernel.

### Manual updates using rpi-update

The `rpi-update` utility will download the latest (unstable, testing) kernel version and copy all required files onto your system. Note that the latest kernel from `rpi-update` is not guaranteed to work correctly! Make sure that it doesn't conflict with your distribution packages. It doesn't provide a way of automatically uninstalling the files.

After upgrading the kernel, you'll have to reboot your Pi to switch to the updated version.

If you're using a compiled kernel, rpi-update will have overwritten it, and you will need to [rebuild](building.md) and reinstall your kernel.

Custom [configurations](configuring.md) can usually be copied over between minor kernel updates, but it's safer to use the `diff` utility to see what's changed and repeat your changes on the new configuration.

### Reverting back to current stock Raspbian kernel

The Raspberry Pi Foundation kernel is part of the `raspberrypi-kernel` package, and the bootloader files are part of the `raspberrypi-bootloader` package. To revert to the current stock Raspbian kernel after trying `rpi-update` or a custom kernel, you need to reinstall both these packages, by running:

```
sudo apt-get install --reinstall raspberrypi-bootloader raspberrypi-kernel
```
