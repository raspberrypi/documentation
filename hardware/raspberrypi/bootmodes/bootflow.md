# Boot flow

The flow of boot begins with reading the OTP to decide on the valid boot modes enabled.  By default this is SD card boot followed by USB device boot.  Subsequently the bootrom checks to see if `program_gpio_bootmode` OTP bit is set, if it is then it reads either GPIOs 22-26 or 39-43 (depending on the value of `program_gpio_bootpos`) and uses those bits to disable boot modes.  This means it is possible to use a hardware switch to switch between different boot modes if there are more than one available.

Next the boot rom checks each of the boot sources for a file called bootcode.bin if it is successfull then it will load the code into the local 128K cache and jump to it.

* Primary SD card boot
* Secondary SD card boot
* NAND boot (currently not supported for Linux booting)
* SPI EEPROM boot (currently not supported for Linux booting)
* USB boot
  * If device mode is set then boot as device
  * If host mode is also set then use OTG bit to decide (Pi B has host enabled)

The primary SD card boot mode is as standard set to be GPIOs 49-53 it is possible (although we've not yet enabled) the ability to boot from the secondary SD card on a second set of pins (i.e. to add a secondary SD card to the GPIO pins).

NAND boot and SPI boot modes do work, although they do not yet have full GPU support.

The USB will boot as a USB device (when plugged into a PC for example) so you can 'squirt' the bootcode.bin into the device.  The code for doing this is [usbboot](https://github.com/raspberrypi/tools/tree/master/usbboot).

Also 2837 has the additional capability to boot as a USB host, if both modes are enabled then the OTG pin on the device is used to select between device and host.  For the Pi 3 this is wired to ground which turns the Pi into a host, but CM3 based designs should use the OTG pin to switch between device and host boot if this is required.
