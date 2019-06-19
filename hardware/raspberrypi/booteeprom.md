# Raspberry Pi 4 boot EEPROM

The Raspberry Pi 4 has an SPI-attached EEPROM (4MBits/512KB), which contains code to boot up the system and replaces `bootcode.bin` previously found in the boot partition of the SD card. Note that if a `bootcode.bin` is present in the boot partition of the SD card in a Pi 4, it is ignored.

## Why use an SPI EEPROM?

 - Pi 4 bootup and SDRAM is considerably more complicated than on the previous Raspberry Pi models, so there is more risk inherent in code that's permanently incorporated in the ROM of the SoC
 - USB has moved to a PCIe bus, and the GENET Ethernet driver is completely different to previous models, so again, having it permanently fixed into the ROM of the SoC was not feasible
 - A small SPI EEPROM allows bugs to be fixed and features to be added after launch, in the field
 - The local modifiable state allows OTP bootmode settings to be removed, and a `recovery.bin` file can be used to revert the Pi to a known working state. This means it's much harder to permanently brick a Pi 4.

## recovery.bin

If the EEPROM needs updating or has somehow become corrupted, it can be reflashed using a fresh SD card with a copy of `recovery.bin` in the first partition of an SD card, formatted to FAT.

`recovery.bin` is a special utility which runs directly from the SD card and updates the EEPROM — it is not in itself a bootloader. It flashes the green LED rapidly (forever) upon success. Because it's not a bootloader, it won't load `start*.elf`, so once you see the green LED flashing rapidly, just re-insert a regular Raspbian SD card and reboot the Pi.
