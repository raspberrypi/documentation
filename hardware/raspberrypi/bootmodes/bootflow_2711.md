# Raspberry Pi4, Pi400 and CM4 bootflow

This page describes the bootflow for BCM2711 based products. The main difference betweeen this and previous products is that the second stage bootloader (bootcode.bin) is loaded for an SPI flash [EEPROM](../booteeprom.md) instead of bootable media. Consequently, settings which previously could only be configured with a one off OTP update may now be modified later on by reflashing the EEPROM.

The bootflow is as follows:-

* BCM2711 SoC powers up
* Read OTP to determine GPIO configuration for second stage loading.
* If nRPIBOOT pin is not defined in OTP or nRPIBOOT GPIO is high
   * Check primary SD/EMMC for recovery.bin
      * Success - run recovery.bin
      * Fail - continue
   * Check SPI EEPROM for second stage loader
      * Success - run second stage bootloader 
      * Fail - continue
* While True
   * Attempt to load recovery.bin from [USB device boot](../computemodule/cm-emmc-flashing.md)
      * Success - run recovery.bin
      * Fail - continue

## recovery.bin
Recovery.bin is a cutdown version of the bootloader which has just enough functionality to reflash the full bootloader in SPI EEPROM.

# Second stage bootloader 

Bootfloat after ROM has loaded the second stage bootloader into the VPU L2 cache:-

* Initialise clocks and SDRAM
* Read EEPROM configuration file
* While True
   * Read the next boot-mode from the BOOT_ORDER field
   * If boot-mode i== SD CARD
      * Attempt to load firmware from the SD card
         * Success - run firmware
         * Failure - continue
   * else if boot-mode == 


## BOOT_ORDER

The `BOOT_ORDER` configuration item is embedded inside the bootloader code in the EEPROM. See the [Pi4 Bootloader Configuration](../bcm2711_bootloader_config.md) page for details on how to change the bootloader configuration.

