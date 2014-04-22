# Updating the Kernel

If you are using the Raspberry Pi stock kernel, your system can be kept up to date by the `rpi-update` utility:

```
$ sudo rpi-update
```

This will install the latest packages, including the Linux kernel image. You will have to reboot your Pi after upgrading the kernel to switch to the updated kernel.

If you are using a compiled kernel you will need to [rebuild](building.md) your kernel again.

Custom [configurations](configuring.md) can usually be copied over between minor kernel updates, but it's safer to use the diff utility to see what's changed and repeat your changes on the new configuration.
