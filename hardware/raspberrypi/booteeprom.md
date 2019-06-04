# Raspberry Pi 4 Boot EEPROM

The Raspberry Pi 4 has an SPI attached EEPROM (4MBits) which contains code to boot up the system, replacing `bootcode.bin` previously found in the boot partition of the SD card. Note that if a `bootcode.bin` is present in the boot partition of the SD card in a Pi4, it is ignored.

## Why use an SPI EEPROM?

 - Pi4 bootup and SDRAM is considerably more complicated than on the previous Raspberry Pi models, so there is more risk in code that is permanently incorproated in the ROM of the SoC.
 - USB has moved to a PCIe bus and the GENET ethernet driver is completely different to previous models, so again, it being permenently baked into the ROM of the SoC was not feasible.
 - A small SPI EEPROM allows bugs to be fixed and features to be added after launch, in the field.
 - The local modifiable state allows OTP bootmode settings to be removed. A `recovery.bin` file can be used to revert your Pi to a known good state so it's much harder to permanently brick a Pi4
 

## recovery.bin

If the EEPROM need updating or has somehow become corrupted, it can be reflashed using a fresh SD card with a copy on `recovery.bin` in the root folder.

`recovery.bin` is a special utility which runs directly from the SD card and updates the EEPROM, it is not in itself a bootloader. It flashes the green LED rapidly (forever) upon success. Because it's not a bootloader, it won't load `start*.elf` so once the flashing is complete, just re-insert a regular Raspbian SD card after the update and reboot.



