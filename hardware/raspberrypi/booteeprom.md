# Raspberry Pi 4 boot EEPROM

The Raspberry Pi 4 has an SPI-attached EEPROM (4MBits/512KB), which contains code to boot up the system and replaces `bootcode.bin` previously found in the boot partition of the SD card. Note that if a `bootcode.bin` is present in the boot partition of the SD card in a Pi 4, it is ignored.

## Why use an SPI EEPROM?

 - Raspberry Pi 4 bootup procedure and SDRAM setup is considerably more complicated than on the previous Raspberry Pi models, so there is more risk inherent in code that's permanently incorporated in the ROM of the SoC.
 - USB has moved to a PCIe bus, and the Gigabit Ethernet driver is completely different to previous models, so again, having it permanently fixed into the ROM of the SoC was not feasible.
 - A small SPI EEPROM allows bugs to be fixed and features to be added after launch, in the field.
 - The local modifiable state means that OTP bootmode settings will not be required for PXE or USB mass storage boot on the Raspberry Pi 4. There are no user modifiable OTP bootmode bits on Pi4.

## PXE and USB Boot

Support for these additional bootmodes will be added in the future via optional bootloader updates. The current schedule is to release PXE boot first, then USB boot.

## Is the bootloader working correctly?

To check that the bootloader is working correctly, turn off the power, unplug everything from the Raspberry Pi 4, including the SD card, and then turn the power back on. If the green LED blinks with a repeating pattern then the bootloader is running correctly, and indicating that `start*.elf` has not been found. Any other actions imply that the bootloader is not working correctly and should be reinstalled using `recovery.bin`.

## recovery.bin

If the EEPROM needs updating or has somehow become corrupted, it can be reflashed using a fresh SD card with a copy of `recovery.bin` in the first partition of an SD card, formatted to FAT.

`recovery.bin` is a special utility which runs directly from the SD card and updates the EEPROM — it is not in itself a bootloader. It flashes the green LED rapidly (forever) upon success. Because it's not a bootloader, it won't load `start*.elf`, so once you see the green LED flashing rapidly, just re-insert a regular Raspbian SD card and reboot the Pi.

It can be downloaded from the [raspberrypi.org downloads page](https://www.raspberrypi.org/downloads/).

## Write protection of EEPROM

Raspbian will not update either the boot EEPROM or the VLI EEPROM (USB controller) without asking for the user's permission. However, it is possible to physically write-protect both EEPROMs via a simple resistor change on the board. Details will be published in the [schematics](./schematics/README.md).

