# Pi4 Bootflow

The Pi4 with the BCM2711 SoC has a new, more sophisticated boot process. The addition of an EEPROM means that the `bootcode.bin` file found in `/boot` is no longer required. Details of the EEPROM can be found [here](../booteeprom.md).

The boot flow for the Pi4 is as follows:

* BCM2711 SoC powers up
* On board bootrom checks for bootloader recovery file (recovery.bin) on the SD card. If found, it executes it to flash the EEPROM and recovery.bin triggers a reset.
* Otherwise, the bootrom loads the main bootloader from the EEPROM.
* Bootloader checks it's inbuilt BOOT_ORDER configuration item to determine what type of boot to do.
  * SD Card
  * Network
  * USB mass storage


## SD Card Boot
The bootloader loads the files in the [boot folder](../../../configuration/boot_folder.md) according to the [boot options](../../../configuration/config-txt/boot.md) in config.txt

## Network boot

Details of the network booting can be found [here](../bcm2711_bootloader_config.md)

## USB mass storage boot

USB booting is still under development.


## BOOT_ORDER

The `BOOT_ORDER` configuration item is embedded inside the bootloader code in the EEPROM. See the [Pi4 Bootloader Configuration](../bcm2711_bootloader_config.md) page for details on how to change the bootloader configuration.

