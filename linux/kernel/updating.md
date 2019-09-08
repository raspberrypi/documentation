# Updating the kernel

If you use the standard Raspbian update/upgrade process (found [here](../../raspbian/updating.md)), this will automatically update the kernel to the latest stable version. This is the recommended procedure. However, in certain circumstances, you may wish to update to the latest 'bleeding edge' or test kernel.

### Manual updates using rpi-update

**Do not use `rpi-update` unless you have been recommended to do so by a Raspberry Pi engineer. This is because it updates the Linux kernel and Raspberry Pi firmware to the very latest version which is currently under test. It may therefore make your Pi unstable, or cause random breakage.**

To use rpi-update, execute it using sudo as follows:

```
sudo rpi-update
```

The `rpi-update` utility will download the Linux kernel and Raspberry Pi firmware that are currently being tested and install them onto your Pi. Note that `rpi-update` does not provide a way to revert the changes that it makes to your system.

After upgrading the kernel, you must reboot your Pi to switch to the updated version.

If you're using a compiled kernel, rpi-update will overwrite it, and you will need to [rebuild](building.md) and reinstall your kernel.

Custom [configurations](configuring.md) can usually be copied over between minor kernel updates, but it's safer to use the `diff` utility to see what's changed and repeat your changes on the new configuration.

### Reverting back to current stock Raspbian kernel

The Raspberry Pi Foundation kernel is supplied by the `raspberrypi-kernel` package, and the bootloader and firmware are supplied by the `raspberrypi-bootloader` package. To revert to the current stock Raspbian kernel after trying `rpi-update` or a custom kernel, you need to reinstall both these packages as follows:

```
sudo apt update
sudo apt install --reinstall raspberrypi-bootloader raspberrypi-kernel
```

Note that this will install the latest stable versions of the kernel, bootloader and firmware that are available from the package repository, which may not be the same versions that you were running before you ran `rpi-update`.
