# Raspberry Pi 4 boot EEPROM

The Raspberry Pi 4 has an SPI-attached EEPROM (4MBits/512KB), which contains code to boot up the system and replaces `bootcode.bin` previously found in the boot partition of the SD card. Note that if a `bootcode.bin` is present in the boot partition of the SD card in a Pi 4, it is ignored.

## Boot diagnostics
If an error occurs during boot then an [error code](../../configuration/led_blink_warnings.md) will be displayed via the green LED. Newer versions of the bootloader will display a [diagnostic message](boot_diagnostics.md) which will be shown on both HDMI displays.

## Updating the bootloader

## Compute Module 4
Bootloader EEPROM updates on Compute Module 4 require [rpiboot](https://github.com/raspberrypi/usbboot) which is also used for flashing the EMMC. Please see the [Compute Module flashing guide](../computemodule/cm-emmc-flashing.md) for instructions.

### Raspberry Pi Imager
The easiest way to to update the bootloader to the latest version with default settings is to use the [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/) to install a boot recovery image onto a spare SD card.

Select "Choose OS -> Misc utility images -> Raspberry Pi 4 EEPROM boot recovery"

Raspberry Pi OS also keeps the EEPROM up-to-date: new EEPROM images are applied when the Raspberry Pi 4 next boots.

### Updating from Raspberry Pi OS
Bootloader updates are instigated during a normal `apt update`, `apt full-upgrade` cycle, this means you will get new features and bug fixes during your normal updates. 

Bootloader updates are performed by `rpi-eeprom-update` service provided by the `rpi-eeprom` package. This service runs at boot and updates the bootloader at the next reboot if a new production release is available. The service automatically migrates the current boot settings to the new bootloader release.

To update your system, including the bootloader:
```
sudo apt update
sudo apt full-upgrade
sudo reboot
```

## Manually checking if an update is available
Running the `rpi-eeprom-update` command with no parameters indicates whether an update is required. An update is required if the version of the most recent file in the firmware directory (normally `/lib/firmware/raspberrypi/bootloader/default`) is newer than that reported by the current bootloader.
The images under `/lib/firmware/raspberrypi/bootloader` are part of the `rpi-eeprom` package and are only updated via `apt upgrade`.

```
sudo rpi-eeprom-update
```

If an update is available, you can install it using:
```
sudo rpi-eeprom-update -a
sudo reboot
```

### Reading the current EEPROM version
```
vcgencmd bootloader_version
```

## Updating the EEPROM configuration
The bootloader EEPROM image contains an embedded configuration file to define the boot behaviour (e.g. selecting between SD, network and USB boot). 
The `rpi-eeprom-config` tool may be used to modify embedded configuration file in an EEPROM image file. 

See the [Bootloader Configuration Page](./bcm2711_bootloader_config.md) for details of the configuration file.

### Reading the current EEPROM configuration
To view the configuration file used by the bootloader at boot time run `rpi-eeprom-config` or `vcgencmd bootloader_config`.

### Reading the configuration file from an EEPROM image
To read the configuration file from an EEPROM image file:
```
rpi-eeprom-config pieeprom.bin
```

### Editing the current bootloader configuration
The following command loads the current EEPROM configuration into a text editor. When the editor is closed, `rpi-eeprom-config` applies the updated configuration to latest available EEPROM release and uses `rpi-eeprom-update` to schedule an update when the system is rebooted:

```
sudo -E rpi-eeprom-config --edit
sudo reboot
```
If the updated configuration file is identical or empty then no changes are made.

The editor is selected by the `EDITOR` environment variable.

### Applying a saved configuration file
The following command applies `boot.conf` to the latest available EEPROM image and uses `rpi-eeprom-update` to schedule an update when the system is rebooted.
```
sudo rpi-eeprom-config --apply boot.conf
sudo reboot
```

### Low level commands

#### Updating the configuration in an EEPROM image
The following command reads `pieeprom.bin` and replaces the configuration file with the contents of `boot.conf`. The result is written to `new.bin`
```
rpi-eeprom-config --config boot.conf --out new.bin pieeprom.bin
```

For more information about advanced options please run `rpi-eeprom-config -h`.

#### Updating the bootloader EEPROM
The following will cause the bootloader EEPROM to be updated the next time the system is rebooted.
```
# -d instructs rpi-eeprom-update to use the EEPROM configuration inside new.bin instead of
# of replacing it with the current configuration from vcgencmd bootloader.
sudo rpi-eeprom-update -d -f new.bin
```
For more information about advanced options please run `rpi-eeprom-update -h`.

### recovery.bin
At power on, the BCM2711 ROM looks for a file called `recovery.bin` in the root directory of the boot partition on the sd-card. If a valid `recovery.bin` is found then the ROM executes this instead of the SPI EEPROM image. This mechanism ensures that the bootloader SPI EEPROM can always be reset to a valid image with factory default settings.

#### EEPROM update files
| Filename | Purpose |
|----------|---------|
| recovery.bin | VideoCore EEPROM recovery executable |
| pieeprom.upd | Bootloader EEPROM image |
| pieeprom.bin | Bootloader EEPROM image - same as pieeprom.upd but changes recovery.bin behaviour |
| pieeprom.sig | The sha256 checksum of bootloader image (pieeprom.upd/pieeprom.bin) |
| vl805.bin | The VLI805 USB firmware EEPROM image - ignored on 1.4 board revision which does not have a dedicated VLI EEPROM|
| vl805.sig | The sha256 checksum of vl805.bin |

* If the bootloader update image is called `pieeprom.upd` then `recovery.bin` renames itself to `recovery.000` and resets the CPU. Since `recovery.bin` is no longer present the ROM loads the newly updated bootloader from SPI EEPROM and the OS is booted as normal.
* If the bootloader update image is called `pieeprom.bin` the `recovery.bin` will stop after the update has completed. On success the HDMI output will be green and the green activity LED is flashed rapidly. Otherwise, the HDMI output will be red and an [error code](../../configuration/led_blink_warnings.md) will be displayed via the activity LED.
* The `.sig` files should just contain the sha256 checksum (in hex) of the corresponding image file. Other fields may be added in the future.
* The BCM2711 ROM does not support loading `recovery.bin` from USB mass storage or TFTP. Instead, newer versions of the bootloader support a self-update mechanism where the SPI bootloader is able to reflash the SPI EEPROM itself. See `ENABLE_SELF_UPDATE` on the [bootloader configuration](bcm2711_bootloader_config.md) page.
* The temporary EEPROM update files are automatically deleted by the `rpi-eeprom-update` service at startup. 

### Firmware release status
The firmware release status corresponds to a particular subdirectory of bootloader firmware images (`/lib/firmware/raspberrypi/bootloader/...`), and can be changed to select a different release stream. By default, Raspberry Pi OS automatically updates the bootloader if 'default' image in the 'rpi-eeprom' image is newer than the current bootloader image. The bootloader EEPROM config is migrated during the upgrade.

* `default` - Updated for new hardware support, critical bug fixes and periodic update for new features that have been tested via the `latest` release.
* `latest` - Updated when new features have been successfully beta tested.
* `beta` - New or experimental features are tested here first.

Since the release status string is just a subdirectory name then it's possible to create your own release streams e.g. a pinned release or custom network boot configuration.

N.B. `default` and `latest` are symbolic links to the older release names of `critical` and `stable`.

### Changing the firmware release

You can change which release stream is to be used during an update by editing the `/etc/default/rpi-eeprom-update` file and changing the `FIRMWARE_RELEASE_STATUS` entry to the appropriate stream. 

For more information about the `rpi-eeprom-update` configuration file please run `rpi-eeprom-update -h`.

### Disabling automatic updates
If you wish to control when the updates are applied you can disable the `rpi-eeprom-update` systemd service.
```
# Disable
sudo systemctl mask rpi-eeprom-update

# Enable it again
sudo systemctl unmask rpi-eeprom-update
```
The `FREEZE_VERSION` option in the [EEPROM config file](bcm2711_bootloader_config.md) may be used to indicate to the `rpi-eeprom-update` service that the EEPROM should not be updated on this board. 

### EEPROM write protect
Write protecting the EEPROMs on the Raspberry Pi 4 Model B requires both a software change and a small board modification. 

**This is only recommended for advanced users or industrial customers.**

By default, neither the bootloader nor the VL805 SPI EEPROMs are write-protected. 

If `eeprom_write_protect=1` is defined in `config.txt` then `recovery.bin` will define the write protect regions such that all of both EEPROMS are write-protected. The write-protect region configuration is then made read-only when the write-protect (`/WP`) pin is pulled low. If `eeprom_write_protect=0` is defined then the write-protect regions are cleared. If `eeprom_write_protect` is not defined then the write-protect bits are not modified.

* The `eeprom_write_protect` property requires the `recovery.bin` from the `2020-07-16` bootloader release or newer.
* The `/WP` pin on these EEPROMs only prevents writes to the non-volatile bits of the status register. Therefore, the write regions must be defined in addition to `/WP` being pulled low.
* The `/WP` pin must not be pulled low whilst attempting to change the write-protect status.
* The `/WP` pin for the EEPROMs may be pulled low by connecting test point 5 (`TP5`) to ground.
* The bootloader self-update mechanism also supports the `eeprom_write_protect` property. However, the bootloader must have already have been upgraded to `2020-07-16` or newer before the `eeprom_write_protect` property will be recognised.

N.B `flashrom` does not support clearing of the write-protect regions and will fail to update the EEPROM if write-protect regions are defined.

## Release Notes
* [Release notes](https://github.com/raspberrypi/rpi-eeprom/blob/master/firmware/release-notes.md) for bootloader EEPROMs.
