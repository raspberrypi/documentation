# Pi4 Bootflow

The Pi4 with the BCM2711 SoC has a new, more sophisticated boot process. The addition of an EEPROM means that the bootload.bin file found in `config.txt` is no longer required. Details of the EEPROM can be found [here](./booteeprom.md).

The boot flow for the Pi4 is as follows:

* BCM2711 SoC powers up
* On board bootrom checks for bootloader recovery file (recovery.bin) on the sd-card. If found, it executes it to flash the EEPROM and recovery.bin triggers a reset.
* Otherwise, the bootrom loads the main bootloader from the EEPROM.
* Bootloader


## SD Card Boot
The bootloader loads the files in the [boot folder](https://www.raspberrypi.org/documentation/configuration/boot_folder.md) according to the [boot options](https://www.raspberrypi.org/documentation/configuration/config-txt/boot.md) in config.txt

## Network boot (BETA)

Details of the network booting can be found [here](https://github.com/raspberrypi/rpi-eeprom/blob/master/firmware/raspberry_pi4_network_boot_beta.md)

## USB mass storage boot

USB booting is still under development

