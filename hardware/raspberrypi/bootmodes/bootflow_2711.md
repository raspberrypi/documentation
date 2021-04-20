# Raspberry Pi 4 boot flow

This page describes the boot flow for BCM2711-based products. The main difference betweeen this and previous products is that the second stage bootloader is loaded from an SPI flash [EEPROM](../booteeprom.md) instead of the `bootcode.bin` file on previous products.

## First stage bootloader

The boot flow for the ROM (first stage) is as follows:-

* BCM2711 SoC powers up
* Read OTP to determine if the `nRPIBOOT` GPIO is configured
* If `nRPIBOOT` GPIO is high or OTP does NOT define `nRPIBOOT` GPIO
   * Check OTP to see if `recovery.bin` can be loaded from SD/EMMC
      * If SD recovery.bin is enabled then check primary SD/EMMC for `recovery.bin`
         * Success - run `recovery.bin` and update the SPI EEPROM
         * Fail - continue
   * Check SPI EEPROM for second stage loader
      * Success - run second stage bootloader
      * Fail - continue
* While True
   * Attempt to load recovery.bin from [USB device boot](../../computemodule/cm-emmc-flashing.md)
      * Success - run `recovery.bin` and update the SPI EEPROM or switch to USB mass storage device mode
      * Fail - retry USB device boot

N.B. Currently only CM4 reserves a GPIO for `nRPIBOOT`.

## recovery.bin
`recovery.bin` is a minimal second stage program used to reflash the bootloader SPI EEPROM image.

## Second stage bootloader

This section describes the high-level flow of the second stage bootloader.

Please see the [bootloader configuration](../bcm2711_bootloader_config.md) page for more information about each boot mode and the [boot folder](../../../configuration/boot_folder.md) page for a description of the GPU firmware files loaded by this stage.

* Initialise clocks and SDRAM
* Read the EEPROM configuration file
* Check `PM_RSTS` register to determine if HALT is requested
   * Check `POWER_OFF_ON_HALT` and `WAKE_ON_GPIO` EEPROM configuration settings.
   * If `POWER_OFF_ON_HALT` is `1` and `WAKE_ON_GPIO` is `0` then
      * Use PMIC to power off system
   * else if `WAKE_ON_GPIO` is `1`
      * Enable fall-edge interrupts on GPIO3 to wake-up if GPIO3 is pulled low
   * sleep
* While True
   * Read the next boot-mode from the BOOT_ORDER parameter in the EEPROM config file.
   * If boot-mode == `RESTART`
      * Jump back to the first boot-mode in the `BOOT_ORDER` field
   * else if boot-mode == `STOP`
      * Display start.elf not found [error pattern](../../../configuration/led_blink_warnings.md) and wait forever.
   * else if boot-mode == `SD CARD`
      * Attempt to load firmware from the SD card
         * Success - run the firmware
         * Failure - continue
   * else if boot-mode == `NETWORK` then
      * Use DHCP protocol to request IP address
      * Load firmware from the DHCP or statically defined TFTP server
      * If the firmware is not found or a timeout or network error occurs then continue
   * else if boot-mode == `USB-MSD` or boot-mode == `BCM-USB-MSD` then
      * While USB discover has not timed out
         * Check for USB mass storage devices
         * If a new mass storage device is found then
            * For each drive (LUN)
               * Attempt to load firmware
                  * Success - run the firmware
                  * Failed - advance to next LUN
   * else if boot-mode == `NVME` then
      * Scan PCIe for an NVMe device and if found
         * Attempt to load firmware from the NVMe device
            * Success - run the firmware
            * Failure - continue
   * else if boot-mode == `RPIBOOT` then
      * Attempt to load firmware using USB device mode from the USB OTG port - see [usbboot](https://github.com/raspberrypi/usbboot). There is no timeout for `RPIBOOT` mode.

## Bootloader updates
The bootloader may also be updated before the firmware is started if a `pieeprom.upd` file is found. Please see the [bootloader EEPROM](../booteeprom.md) page for more information about bootloader updates.
