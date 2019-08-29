# Raspberry Pi 4 boot EEPROM

The Raspberry Pi 4 has an SPI-attached EEPROM (4MBits/512KB), which contains code to boot up the system and replaces `bootcode.bin` previously found in the boot partition of the SD card. Note that if a `bootcode.bin` is present in the boot partition of the SD card in a Pi 4, it is ignored.

## Why use an SPI EEPROM?

 - Raspberry Pi 4 bootup procedure and SDRAM setup is considerably more complicated than on the previous Raspberry Pi models, so there is more risk inherent in code that's permanently incorporated in the ROM of the SoC.
 - USB has moved to a PCIe bus, and the Gigabit Ethernet driver is completely different to previous models, so again, having it permanently fixed into the ROM of the SoC was not feasible.
 - A small SPI EEPROM allows bugs to be fixed and features to be added after launch, in the field.
 - The local modifiable state means that OTP bootmode settings will not be required for PXE or USB mass storage boot on the Raspberry Pi 4. There are no user-modifiable OTP bootmode bits on Pi 4.

## PXE and USB Boot

Support for these additional bootmodes will be added in the future via optional bootloader updates. The current schedule is to release PXE boot first, then USB boot.

## Is the bootloader working correctly?

To check that the bootloader is working correctly, turn off the power, unplug everything from the Raspberry Pi 4, including the SD card, and then turn the power back on. If the green LED blinks with a repeating pattern then the bootloader is running correctly, and indicating that `start*.elf` has not been found. Any other actions imply that the bootloader is not working correctly and should be reinstalled using `recovery.bin`.

## recovery.bin

If the EEPROM needs updating or has somehow become corrupted, it can be reflashed using a fresh SD card with a copy of `recovery.bin` in the first partition of an SD card, formatted to FAT32.

`recovery.bin` is a special utility which runs directly from the SD card and updates the EEPROM — it is not in itself a bootloader. It flashes the green LED rapidly (forever) upon success. Because it's not a bootloader, it won't load `start*.elf`, so once you see the green LED flashing rapidly, just re-insert a regular Raspbian SD card and reboot the Pi.

It can be downloaded from the [raspberrypi.org downloads page](https://www.raspberrypi.org/downloads/).

## Write protection of EEPROM

There is no software write protection for the boot EEPROM but there will be a mechanism in Raspbian to skip any future updates to the EEPROM. However, it is possible to physically write-protect both EEPROMs via a simple resistor change on the board. Details will be published in the [schematics](./schematics/README.md).

## EEPROM configuration options

The EEPROM image contains a small user-modifiable config file. To change a setting:

* Download and unzip the rescue bootloader image from https://www.raspberrypi.org/downloads/
* Used sed to change setting. Be careful to avoid changing anything else otherwise it will fail to boot.
  * `sed -i -e "s/BOOT_UART=0/BOOT_UART=1/" pieeprom.bin`
* Flash the image - see embedded README.txt in rescue image zip.

We will soon be releasing a tool which allows the EEPROM config to be extracted and modified without having to use sed hacks.

#### BOOT_UART

If 1 then enable UART debug output on GPIO 14 and 15. Configure the debug terminal at 115200bps, 8 bits, no parity bits, 1 stop bit. 
Default: 0  
Version: All  

#### WAKE_ON_GPIO 

If 1 then 'sudo halt' will run in a lower power mode until either GPIO3 or GLOBAL_EN are shorted to ground.  

Default: 0 in original version of bootloader (2019-05-10). Newer bootloaders have this set to 1.  
Version: All  

#### POWER_OFF_ON_HALT  

If 1 and WAKE_ON_GPIO=0 then switch off all PMIC outputs in halt. This is lowest possible power state for halt but may cause problems with some HATs because 5V will still be on. GLOBAL_EN must be shorted to ground to boot.  

Default: 0  
Version: 2019-07-15  

#### FREEZE_VERSION

If 1 then the Raspbian EEPROM update service (rpi-eeprom package) will skip automatic updates on this board. The parameter is not processed by the EEPROM bootloader or recovery.bin since there is no way in software of fully write protecting the EEPROM. Custom EEPROM update scripts must also check for this flag.

Default: 0  
Version: All  

# Release Notes for production versions
## 2019-07-15 - RC3.3 - Git 514670a2
   * Turn green LED activity off on halt.
   * Pad embedded config file with spaces for easier editing by end users.
   * Halt now behaves the same as earlier Pi models to improve power behavior at halt for HATs. 
      * WAKE_ON_GPIO now defaults to 1 in the EEPROM config file.
      * POWER_OFF_ON_HALT setting added defaulting to zero. Set this to 1 to restore the behavior where 'sudo halt' powers off all PMIC output.
      * If WAKE_ON_GPIO=1 then POWER_OFF_ON_HALT is ignored.
   * Load start4db.elf / fixup4db.dat in preference to start_db.elf / fixup_db.dat on Pi4.
   * Embed BUILD_TIMESTAMP in the EEPROM image to assist version checking.
## 2019-05-10 RC2.1 - Git d2402c53
   * First production version 
