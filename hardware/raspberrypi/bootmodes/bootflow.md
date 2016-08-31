# Boot flow

The flow of boot begins with reading the OTP to decide on the valid boot modes enabled. By default this is SD card boot followed by USB device boot. Subsequently, the boot ROM checks to see if `program_gpio_bootmode` OTP bit is set, if it is then it reads either GPIOs 22-26 or 39-43 (depending on the value of `program_gpio_bootpos`) and uses those bits to disable boot modes.  This means it is possible to use a hardware switch to switch between different boot modes if there are more than one available.

Next the boot ROM checks each of the boot sources for a file called bootcode.bin; if it is successful it will load the code into the local 128K cache and jump to it. The overall boot mode process is as follows:

* 2837 boots
* Reads boot ROM enabled boot modes from OTP
* Uses gpio_bootmode to disable some modes by reading GPIOs 22-26 or 39-43 to see if the default values do not equal the default pull to '0'.  If it is low it will disable that boot mode for each of SD1, SD2, NAND, SPI, USB. If the value read is a '1' then that boot mode is enabled, note this cannot enable boot modes that have not already been enabled in the OTP. The default pull resistance is around 50k ohms, so a smaller pull up of 5K should suffice to enable the boot mode but still allow the GPIO to be operational without consuming too much power.
* If enabled: Check primary SD for bootcode.bin
  * Success - Boot
  * Fail - timeout (5 seconds)
* If enabled: Check secondary SD
  * Sucess - Boot
  * Fail - timeout (5 seconds)
* If enabled: Check NAND
* If enabled: Check SPI
* If enabled: Check USB
  * If OTG pin == 0 
    * Enable USB, wait for valid USB 2.0 devices (2 seconds)
      * Device found:
        * If device type == hub
          * Recurse for each port
        * If device type == (mass storage or LAN9500)
          * Store in list of devices
    * Recurse through each MSD
      * If bootcode.bin found boot
    * Recurse through each LAN9500
      * DHCP / TFTP boot
  * else (Device mode boot)
    * Enable device mode and wait for host PC to enumerate
    * We reply to PC with VID: 0a5c PID: 0x2763 (Pi 1 or Pi 2) or 0x2764 (Pi 3)

NOTES: 

* If there is no SD card inserted the SD boot mode takes five seconds to fail. To reduce this and fall back to USB more quickly, you can either insert an SD card with nothing on it or use the `program_gpio_bootmode` OTP to only enable USB.
* The default pull for the GPIOs is defined on page 102 of the [ARM Peripherals datasheet](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bcm2835/BCM2835-ARM-Peripherals.pdf) if the value at boot time does not equal the default pull then that boot mode is enabled.
* USB enumeration is a mechanism of enabling the power to the downstream devices on a hub then waiting for the devices to pull the D+ and D- lines to indicate it is either USB 1 or USB 2. This can take time and on some devices it can take up to 3 seconds for a hard disk drive to spin up and start the enumeration process. Because this is the only way of detecting the hardware is attached we have to sit waiting for a minimum amount of time (2 seconds) if the device fails to respond after this maximum timeout it is possible to increase the timeout to 5 seconds using `program_usb_timeout=1` in config.txt
* MSD takes precedence over ethernet boot
* It is no longer necessary for the first partition to be the FAT partition, the MSD boot will continue to search for a FAT partition beyond the first one.
* The boot ROM also now supports GUID partitioning and has been tested with hard drives partitioned using Mac, Windows and Linux.

The primary SD card boot mode is as standard set to be GPIOs 49-53 it is possible (although we've not yet enabled) the ability to boot from the secondary SD card on a second set of pins (i.e. to add a secondary SD card to the GPIO pins).

NAND boot and SPI boot modes do work, although they do not yet have full GPU support.

By default the USB device boot mode is enabled at manufacture time, but the USB host boot mode is only enabled with the `program_usb_boot_mode=1` once enabled the processor will use the value of the OTGID pin on the processor to decide between the two modes. On a Raspberry Pi Model B the OTGID pin is driven to '0' and therefore will only boot via host mode once enabled (it is not possible to boot through device mode because of the LAN9515 device in the way)

The USB will boot as a USB device on Pi Zero or Compute Module if the OTGID pin is left floating (when plugged into a PC for example) so you can 'squirt' the bootcode.bin into the device. The code for doing this is [usbboot](https://github.com/raspberrypi/tools/tree/master/usbboot).

