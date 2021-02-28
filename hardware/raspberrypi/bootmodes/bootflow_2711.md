# Raspberry Pi4, Pi400 and CM4 bootflow

This page describes the bootflow for BCM2711 based products. The main difference betweeen this and previous products is that the second stage bootloader (bootcode.bin) is loaded from an SPI flash [EEPROM](../booteeprom.md). 

The bootflow for the ROM (first stage) is as follows:-

* BCM2711 SoC powers up
* Read OTP to determine GPIO configuration for second stage loading.
* If nRPIBOOT GPIO is high or OTP does not define nRPIBOOT GPIO (only defined for CM4)
   * Check primary SD/EMMC for recovery.bin
      * Success - run `recovery.bin`
      * Fail - continue
   * Check SPI EEPROM for second stage loader
      * Success - run second stage bootloader 
      * Fail - continue
* While True
   * Attempt to load recovery.bin from [USB device boot](../computemodule/cm-emmc-flashing.md)
      * Success - run `recovery.bin`
      * Fail - retry USB device boot

## recovery.bin
`recovery.bin` is a minimal second stage program used to reflash the bootloader SPI EEPROM image.

# Second stage bootloader 

This section describes the high-level flow of the second stage bootloader.

Please see the [bootloader configuration](../bcm2711_bootloader_config.md) page for more information about each boot-mode and the [boot folder](../../../configuration/boot_folder.md) page for a description of the GPU firmware files loaded by this stage.

* Initialise clocks and SDRAM
* Check PM_RSTS register to determine if HALT is requested
   * If POWER_OFF_ON_HALT = 1 and WAKE_ON_GPIO = 0 then
      * Use PMIC to power off system
   * else
      * While GPIO3 is high OR WAKE_ON_GPIO = 1
         Sleep
* Read the EEPROM configuration file 
* While True
   * Read the next boot-mode from the BOOT_ORDER parameter in the EEPROM config file.
   * If boot-mode == RESTART
      * Jump back to the first boot-mode in the BOOT_ORDER field
   * else if boot-mode == STOP
      * Display start.elf not found [error pattern](../../../configuration/led_blink_warnings.md) and wait forever.
   * else if boot-mode == SD CARD
      * Attempt to load firmware from the SD card
         * Success - run firmware
         * Failure - continue
   * else if boot-mode == NETWORK
      * If boot-mode == NETWORK then 
         * Used DHCP to request IP address
         * Load firmware from TFTP server
         * If the firmware is not found or a timeout or network error occurs then continue
   * else if boot-mode == USB-MSD or boot-mode == USB-BCM-MSD then
      * While USB discover has not timed out 
         * Check for USB mass storage devices
         * If a new mass storage device is found then
            * For each drive (LUN)
               * Attempt to load firmware
                  * Success - run firmware
                  * Failed - advance to next LUN
   * else if boot-mode == RPIBOOT then
      * Attempt to load firmware using USB device mode from the USB OTG port- see [usbboot](https://github.com/raspberrypi/usbboot) There is no timeout for RPIBOOT mode.
         
