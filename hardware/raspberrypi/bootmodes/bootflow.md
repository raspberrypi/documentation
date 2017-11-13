# Boot flow

The flow of boot begins with reading the OTP to decide on the valid boot modes enabled. By default, this is SD card boot followed by USB device boot. Subsequently, the boot ROM checks to see if the GPIO boot mode OTP bits have been programmed — one to enable GPIO boot mode and one to select the bank of GPIOs it uses to disable boot modes (low = GPIOs 22-26, high = GPIOs 39-43). This makes it possible to use a hardware switch to choose between different boot modes if there is more than one available.

The GPIO boot mode OTP bits can be programmed by adding `program_gpio_bootmode=n` to `config.txt`, where n is `1` to select the low bank (22-26) or `2` to select the high bank (39-43). Once added, boot the device, then power-cycle it (rebooting is not sufficient). You should expect it to no longer boot (all boot modes will be disabled by default). Apply a pull-up to the required pin to enable the required boot mode. After programming, the `config.txt` setting can be removed.

N.B.:
1. It is important to remember that, **once set, OTP bits can never be unset**, so think carefully before enabling this facility because it effectively makes 5 GPIOs unusable for other purposes. Also note that the bit assignments make it possible to switch from the low bank (22-26) to the high bank (39-43), **but not back again**, and that selecting the high bank is likely to produce a non-bootable Pi, unless you're using a Compute Module (any version).
2. **Do not use `program_gpio_bootmode` unless your firmware is dated 20 Oct 2017 or later (`vcgencmd version`). Doing so will make it impossible to select the low bank of boot mode GPIOs.**

Next the boot ROM checks each of the boot sources for a file called bootcode.bin; if it is successful it will load the code into the local 128K cache and jump to it. The overall boot mode process is as follows:

* 2837 boots
* Reads boot ROM enabled boot modes from OTP
* Uses program_gpio_bootmode to disable some modes by reading GPIOs 22-26 or 39-43 to see if the default values do not equal the default pull to '0'. If it is low, it will disable that boot mode for each of SD1, SD2, NAND, SPI, USB. If the value read is a '1', then that boot mode is enabled (note this cannot enable boot modes that have not already been enabled in the OTP). The default pull resistance is around 50K ohm, so a smaller pull up of 5K should suffice to enable the boot mode but still allow the GPIO to be operational without consuming too much power.
* If enabled: check primary SD for bootcode.bin on GPIO 48-53
  * Success - Boot
  * Fail - timeout (five seconds)
* If enabled: check secondary SD
  * Success - Boot
  * Fail - timeout (five seconds)
* If enabled: check NAND
* If enabled: check SPI
* If enabled: check USB
  * If OTG pin == 0 
    * Enable USB, wait for valid USB 2.0 devices (two seconds)
      * Device found:
        * If device type == hub
          * Recurse for each port
        * If device type == (mass storage or LAN951x)
          * Store in list of devices
    * Recurse through each MSD
      * If bootcode.bin found boot
    * Recurse through each LAN951x
      * DHCP / TFTP boot
  * else (Device mode boot)
    * Enable device mode and wait for host PC to enumerate
    * We reply to PC with VID: 0a5c PID: 0x2763 (Pi 1 or Pi 2) or 0x2764 (Pi 3)

NOTES: 

* If there is no SD card inserted, the SD boot mode takes five seconds to fail. To reduce this and fall back to USB more quickly, you can either insert an SD card with nothing on it or use the GPIO bootmode OTP setting described above to only enable USB.
* The default pull for the GPIOs is defined on page 102 of the [ARM Peripherals datasheet](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bcm2835/BCM2835-ARM-Peripherals.pdf). If the value at boot time does not equal the default pull, then that boot mode is enabled.
* USB enumeration is a means of enabling power to the downstream devices on a hub, then waiting for the device to pull the D+ and D- lines to indicate if it is either USB 1 or USB 2. This can take time: on some devices it can take up to three seconds for a hard disk drive to spin up and start the enumeration process. Because this is the only way of detecting that the hardware is attached, we have to wait for a minimum amount of time (two seconds). If the device fails to respond after this maximum timeout, it is possible to increase the timeout to five seconds using `program_usb_timeout=1` in `config.txt`.
* MSD takes precedence over Ethernet boot.
* It is no longer necessary for the first partition to be the FAT partition, as the MSD boot will continue to search for a FAT partition beyond the first one.
* The boot ROM also now supports GUID partitioning and has been tested with hard drives partitioned using Mac, Windows, and Linux.
* The LAN951x is detected using the Vendor ID 0x0424 and Product ID 0xec00, this is different to the standalone LAN9500 device which has a product ID of 0x9500 or 0x9e00.  To use the standalone LAN9500 an I2C EEPROM would need to be added to change these ID's to match the LAN9514

The primary SD card boot mode is, as standard, set to be GPIOs 49-53. It is possible to boot from the secondary SD card on a second set of pins, i.e. to add a secondary SD card to the GPIO pins. However, we have not yet enabled this ability.

NAND boot and SPI boot modes do work, although they do not yet have full GPU support.

The USB device boot mode is enabled by default at the time of manufacture, but the USB host boot mode is only enabled with `program_usb_boot_mode=1`. Once enabled, the processor will use the value of the OTGID pin on the processor to decide between the two modes. On a Raspberry Pi Model B, the OTGID pin is driven to '0' and therefore will only boot via host mode once enabled (it is not possible to boot through device mode because the LAN9515 device is in the way).

The USB will boot as a USB device on the Pi Zero or Compute Module if the OTGID pin is left floating (when plugged into a PC for example), so you can 'squirt' the bootcode.bin into the device. The code for doing this is [usbboot](https://github.com/raspberrypi/usbboot).

