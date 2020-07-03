# Raspberry Pi 4 boot EEPROM

The Raspberry Pi 4 has an SPI-attached EEPROM (4MBits/512KB), which contains code to boot up the system and replaces `bootcode.bin` previously found in the boot partition of the SD card. Note that if a `bootcode.bin` is present in the boot partition of the SD card in a Pi 4, it is ignored.

## Why use an SPI EEPROM?

 - Raspberry Pi 4 bootup procedure and SDRAM setup is considerably more complicated than on the previous Raspberry Pi models, so there is more risk inherent in code that's permanently incorporated in the ROM of the SoC.
 - USB has moved to a PCIe bus, and the Gigabit Ethernet driver is completely different to previous models, so again, having it permanently fixed into the ROM of the SoC was not feasible.
 - A small SPI EEPROM allows bugs to be fixed and features to be added after launch, in the field.
 - The local modifiable state means that OTP bootmode settings will not be required for network or USB mass storage boot on the Raspberry Pi 4. There are no user-modifiable OTP bootmode bits on Pi 4.

## USB boot

USB boot support is currently being beta-tested. See the "USB mass storage boot" section of the [Bootloader Configuration Page](./bcm2711_bootloader_config.md) for further details.

## Is the bootloader working correctly?

To check that the bootloader is working correctly, turn off the power, unplug everything from the Raspberry Pi 4, including the SD card, and then turn the power back on. If the green LED blinks with a repeating pattern then the bootloader is running correctly, and indicating that `start*.elf` has not been found. Any other actions imply that the bootloader is not working correctly and should be reinstalled using `recovery.bin`.

## Recovery image

If the Raspberry Pi is not booting it's possible that the bootloader EEPROM is corrupted. This can easily be reprogrammed using the Raspberry Pi Imager tool which is available via the [raspberrypi.org downloads page](https://www.raspberrypi.org/downloads/).

Using the recovery image will erase any custom configuration options, resetting the bootloader back to factory defaults.

## Updating the bootloader

Bootloader updates are instigated during a normal `apt update`, `apt full-upgrade` cycle, this means you will get new features and bug fixes during your normal updates. 

Bootloader updates are performed by the `rpi-eeprom` package, which installs a service that runs at boot-time to check for critical updates. 

To update your system, including the bootloader:

```
sudo apt update
sudo apt full-upgrade
sudo reboot
```

If you wish to control when the updates are applied you can disable the systemd service from running automatically and run `rpi-eeprom-update` manually, as shown in the 'Manually checking if an update is available' section below.

```
# Disable
sudo systemctl mask rpi-eeprom-update

# Enable it again
sudo systemctl unmask rpi-eeprom-update
```

The `FREEZE_VERSION` option in the EEPROM config file may be used to indicate that the EEPROM should not be updated on this board. 

Note that by default, updating the bootloader (automatically or manually) will retain any custom configuration options of the previous installed version. You can override the migration by manually updating and using the `-d` option with `rpi-eeprom-update`. This will force the updated bootloader to use its inbuilt defaults.

## Manually checking if an update is available

Running the `rpi-eeprom-update` command with no parameters indicates whether an update is required. An update is required if the timestamp of the most recent file in the firmware directory (normally `/lib/firmware/raspberrypi/bootloader/critical`) is newer than that reported by the current bootloader.
The images under `/lib/firmware/raspberrypi/bootloader` are part of the `rpi-eeprom` package and are only updated via `apt update`.

```
sudo rpi-eeprom-update
```

If an update is available, you can install it using :

```
sudo rpi-eeprom-update -a
sudo reboot
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

### Firmware release status
The firmware release status corresponds to a particular subdirectory of bootloader firmware images (`/lib/firmware/raspberrypi/bootloader/...`), and can be changed to select a different release stream. By default, Raspberry Pi OS only selects critical updates (security fixes or major hardware compatiblity changes) since most users do not use alternate boot modes (TFTP, USB etc)

* critical - Default - rarely updated
* stable - Updated when new/advanced features have been successfully beta tested. 
* beta - New or experimental features are tested here first.

Since the release status string is just a subdirectory name then it's possible to create your own release streams e.g. a pinned release or custom network boot configuration.

### Changing the firmware release

You can change which release stream is to be used during an update by editing the `/etc/default/rpi-eeprom-update` file and changing the `FIRMWARE_RELEASE_STATUS` entry to the appropriate stream.

## EEPROM Bootloader configuration options

See the [Bootloader Configuration Page](./bcm2711_bootloader_config.md) for configuration details.

## Release Notes
* [Release notes](https://github.com/raspberrypi/rpi-eeprom/blob/master/firmware/release-notes.md) for bootloader EEPROMs.


