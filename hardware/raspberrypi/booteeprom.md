# Raspberry Pi 4 boot EEPROM

The Raspberry Pi 4 has an SPI-attached EEPROM (4MBits/512KB), which contains code to boot up the system and replaces `bootcode.bin` previously found in the boot partition of the SD card. Note that if a `bootcode.bin` is present in the boot partition of the SD card in a Pi 4, it is ignored.

## Why use an SPI EEPROM?

 - Raspberry Pi 4 bootup procedure and SDRAM setup is considerably more complicated than on the previous Raspberry Pi models, so there is more risk inherent in code that's permanently incorporated in the ROM of the SoC.
 - USB has moved to a PCIe bus, and the Gigabit Ethernet driver is completely different to previous models, so again, having it permanently fixed into the ROM of the SoC was not feasible.
 - A small SPI EEPROM allows bugs to be fixed and features to be added after launch, in the field.
 - The local modifiable state means that OTP bootmode settings will not be required for network or USB mass storage boot on the Raspberry Pi 4. There are no user-modifiable OTP bootmode bits on Pi 4.

## Network and USB boot

Support for these additional bootmodes will be added in the future via optional bootloader updates. The current schedule is to release network boot first, then USB boot.

## Is the bootloader working correctly?

To check that the bootloader is working correctly, turn off the power, unplug everything from the Raspberry Pi 4, including the SD card, and then turn the power back on. If the green LED blinks with a repeating pattern then the bootloader is running correctly, and indicating that `start*.elf` has not been found. Any other actions imply that the bootloader is not working correctly and should be reinstalled using `recovery.bin`.

## Recovery image

If the Raspberry Pi is not booting it's possible that the bootloader EEPROM is corrupted. This can easily be reprogrammed using the Recovery image available on the [raspberrypi.org downloads page](https://www.raspberrypi.org/downloads/).

## Updating the bootloader

We recommend setting up your Pi so that it automatically updates the bootloader: this means you will get new features and bug fixes as they are released. Bootloader updates are performed by the `rpi-eeprom` package, which installs a service that runs at boot-time to check for critical updates.

```
sudo apt update
sudo apt upgrade
sudo apt install rpi-eeprom
```

If you wish to control when the updates are applied you can disable the systemd service from running automatically and run `rpi-eeprom-update` manually.

```
# Prevent the service from running, this can be run before the package is installed to prevent it ever running automatically.
sudo systemctl mask rpi-eeprom-update

# Enable it again
sudo systemctl unmask rpi-eeprom-update
```

The `FREEZE_VERSION` option in the EEPROM config file may be used to indicate that the EEPROM should not be updated on this board. 

## Write protection of EEPROM

There is no software write protection for the boot EEPROM but there will be a mechanism in Raspbian to skip any future updates to the EEPROM. However, it is possible to physically write-protect both EEPROMs via a simple resistor change on the board. Details will be published in the [schematics](./schematics/README.md).

## EEPROM configuration options

EPROM image files contain a small user-modifiable config file, which may be modified using the `rpi-eeprom-config` script included in the `rpi-eeprom` package.

### Update the EEPROM config
```
# Copy the EEPROM of interest from /lib/firmware/raspberrypi/bootloader/critical/

# To extract the configuration file from an EEPROM image.
rpi-eeprom-config pieeprom.bin --out bootconf.txt

# To update the configuration file in an EEPROM image.
rpi-eeprom-config pieeprom.bin --config bootconf.txt --out pieeprom-new.bin

# To flash the new image
# -d means that the configuration in the file should be used, otherwise, rpi-eeprom-update 
# will automatically migrate the current bootloader's configuration to the new image.
sudo rpi-eeprom-update -d -f ./pieeprom-new.bin
```

### Checking if an update is available
Running the rpi-eeprom-update command with no parameters indicates whether an update is required. An update is required if the timestamp of the most recent file in the firmware directory (normally `/lib/firmware/raspberrypi/bootloader/critical`) is newer than that reported
by the current bootloader.
The images under `/lib/firmware/raspberrypi/bootloader` are part of the `rpi-eeprom` package and are only updated via `apt update`.

```
rpi-eeprom-update
```

### Reading the current EEPROM configuration

To view the configuration file used by the bootloader at boot time
```
vcgencmd bootloader_config
```

### Reading the EEPROM version
```
vcgencmd bootloader_version
```

### Beta firmware
Beta firmware files will be stored in `/lib/firmware/raspberrypi/bootloader/beta/`. Developers or beta-testers who are comfortable with using the rescue image to fix boot problems can track the beta firmware by editing `/etc/default/rpi-eeprom-update` 
```
Change FIRMWARE_RELEASE_STATUS="critical"
to FIRMWARE_RELEASE_STATUS="beta"
```

### Configuration options

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

If 1 then the `rpi-eeprom-update` will skip automatic updates on this board. The parameter is not processed by the EEPROM bootloader or recovery.bin since there is no way in software of fully write protecting the EEPROM. Custom EEPROM update scripts must also check for this flag.

Default: 0  
Version: All  

# Release Notes
* [Release notes](https://github.com/raspberrypi/rpi-eeprom/blob/master/firmware/release-notes.md) for bootloader EEPROMs.
