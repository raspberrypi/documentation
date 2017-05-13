# Device boot

The following devices can boot through the special device boot mode:

* Pi CM
* Pi CM3
* Pi Zero
* Pi Zero W

When this boot mode is activated (usually having failed to boot from SD card), it switches to a USB device and awaits a USB reset from the host.  Example code showing how the host needs to talk to the Pi can be found [here](https://github.com/raspberrypi/usbboot).

The host first sends a structure to the device down control endpoint 0, this contains the size and signature for the boot (security is not enabled so no signature is required).  The 2nd stage code is then transmitted down endpoint 1 (bootcode.bin).  Finally the device will reply with a success code of:

* 0    - Success
* 0x80 - Failed

