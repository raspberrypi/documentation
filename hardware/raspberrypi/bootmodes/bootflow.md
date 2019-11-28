# Boot sequence

**The following boot sequence applies to the BCM2837 and BCM2837B0 based models of Raspberry Pi only. On models prior to this, the Pi will try [SD card boot](sdcard.md), followed by [USB device mode boot](device.md). For the Raspberry Pi4 boot sequence please see [this](bootflow_2711.md) page**

USB boot defaults on the Raspberry Pi 3 will depend on which version is being used. See this [page](./msd.md) for information on enabling USB boot modes when not enabled by default.

When the BCM2837 boots, it uses two different sources to determine which boot modes to enable. Firstly, the OTP (one-time programmable) memory block is checked to see which boot modes are enabled. If the GPIO boot mode setting is enabled, then the relevant GPIO lines are tested to select which of the OTP-enabled boot modes should be attempted. Note that GPIO boot mode can only be used to select boot modes that are already enabled in the OTP. See [GPIO boot mode](gpio.md) for details on configuring GPIO boot mode. GPIO boot mode is disabled by default.

Next, the boot ROM checks each of the boot sources for a file called bootcode.bin; if it is successful it will load the code into the local 128K cache and jump to it. The overall boot mode process is as follows:

* BCM2837 boots
* Read OTP to determine which boot modes to enable
* If GPIO boot mode enabled, use GPIO boot mode to refine list of enabled boot modes 
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
* The default pull for the GPIOs is defined on page 102 of the [ARM Peripherals datasheet](../bcm2835/BCM2835-ARM-Peripherals.pdf). If the value at boot time does not equal the default pull, then that boot mode is enabled.
* USB enumeration is a means of enabling power to the downstream devices on a hub, then waiting for the device to pull the D+ and D- lines to indicate if it is either USB 1 or USB 2. This can take time: on some devices it can take up to three seconds for a hard disk drive to spin up and start the enumeration process. Because this is the only way of detecting that the hardware is attached, we have to wait for a minimum amount of time (two seconds). If the device fails to respond after this maximum timeout, it is possible to increase the timeout to five seconds using `program_usb_boot_timeout=1` in `config.txt`.
* MSD boot takes precedence over Ethernet boot.
* It is no longer necessary for the first partition to be the FAT partition, as the MSD boot will continue to search for a FAT partition beyond the first one.
* The boot ROM also now supports GUID partitioning and has been tested with hard drives partitioned using Mac, Windows, and Linux.
* The LAN951x is detected using the Vendor ID 0x0424 and Product ID 0xec00: this is different to the standalone LAN9500 device, which has a product ID of 0x9500 or 0x9e00.  To use the standalone LAN9500, an I2C EEPROM would need to be added to change these IDs to match the LAN951x.

The primary SD card boot mode is, as standard, set to be GPIOs 49-53. It is possible to boot from the secondary SD card on a second set of pins, i.e. to add a secondary SD card to the GPIO pins. However, we have not yet enabled this ability.

NAND boot and SPI boot modes do work, although they do not yet have full GPU support.

The USB device boot mode is enabled by default at the time of manufacture, but the USB host boot mode is only enabled with `program_usb_boot_mode=1`. Once enabled, the processor will use the value of the OTGID pin on the processor to decide between the two modes. On a Raspberry Pi Model B, the OTGID pin is driven to '0' and therefore will only boot via host mode once enabled (it is not possible to boot through device mode because the LAN9515 device is in the way).

The USB will boot as a USB device on the Pi Zero or Compute Module if the OTGID pin is left floating (when plugged into a PC for example), so you can 'squirt' the bootcode.bin into the device. The code for doing this is [usbboot](https://github.com/raspberrypi/usbboot).

