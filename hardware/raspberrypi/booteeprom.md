# Raspberry Pi 4 boot EEPROM

The Raspberry Pi 4 has an SPI-attached EEPROM (4MBits/512KB), which contains code to boot up the system and replaces `bootcode.bin` previously found in the boot partition of the SD card. Note that if a `bootcode.bin` is present in the boot partition of the SD card in a Pi 4, it is ignored.

## Boot diagnostics
If an error occurs during boot then an [error code](../../configuration/led_blink_warnings.md) will be displayed via the green LED. Newer versions of the bootloader will display a [diagnostic message](boot_diagnostics.md) which will be shown on both HDMI displays.

## Updating the bootloader
### Pi 4 and Pi 400
Raspberry Pi OS automatically updates the bootloader for critical bug fixes. The recommended methods for manually updating the bootloader or changing the boot modes are [Raspberry Pi Imager](https://www.raspberrypi.org/downloads) and [raspi-config](../../configuration/raspi-config.md)

### Compute Module 4
Bootloader EEPROM updates on Compute Module 4 require [rpiboot](https://github.com/raspberrypi/usbboot) which is also used for flashing the EMMC. Please see the [Compute Module flashing guide](../computemodule/cm-emmc-flashing.md) for instructions.

<a name="imager"></a>
### Using Raspberry Pi Imager to update the bootloader (recommended)
Raspberry Pi Imager provides a GUI for updating the bootloader and selecting the boot mode.

1. Download [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/)
2. Select a spare SD card. The contents will get overwritten!
3. Launch `Raspberry Pi Imager`
4. Select `Misc utility images` under `Operating System`
5. Select `Bootloader`
6. Select a boot-mode i.e. `SD` (recommended), `USB` or `Network`.
7. Select `SD card` and then `Write`
8. Boot the Raspberry Pi with the new image and wait for at least 10 seconds.
9. The green activity LED will blink with a steady pattern and the HDMI display will be green on success.
10. Power off the Raspberry Pi and remove the SD card.

<a name="raspi-config"></a>
### Using raspi-config to update the bootloader from within Raspberry Pi OS
To change the boot-mode or bootloader version from within Raspberry Pi OS run [raspi-config](../../configuration/raspi-config.md)

1. [Update](../../raspbian/updating.md) Raspberry Pi OS to get the latest version of the `rpi-eeprom` package.
2. Run `sudo raspi-config`
3. Select `Advanced Options`
4. Select `Bootloader Version`
5. Select `Default` for factory default settings or `Latest` for the latest stable bootloader release.
6. Reboot

## Updating the EEPROM configuration
The boot behaviour (e.g. SD or USB boot) is controlled by a configuration file embedded in the EEPROM image and can be modified via the `rpi-eeprom-config` tool.

Please see the [Bootloader Configuration Page](bcm2711_bootloader_config.md) for details of the configuration.

### Reading the current EEPROM configuration
To view the configuration used by the current bootloader during the last boot run `rpi-eeprom-config` or `vcgencmd bootloader_config`.

### Reading the configuration from an EEPROM image
To read the configuration from an EEPROM image:
```bash
rpi-eeprom-config pieeprom.bin
```
### Editing the current bootloader configuration
The following command loads the current EEPROM configuration into a text editor. When the editor is closed, `rpi-eeprom-config` applies the updated configuration to latest available EEPROM release and uses `rpi-eeprom-update` to schedule an update when the system is rebooted:

```bash
sudo -E rpi-eeprom-config --edit
sudo reboot
```
If the updated configuration is identical or empty then no changes are made.

The editor is selected by the `EDITOR` environment variable.

### Applying a saved configuration
The following command applies `boot.conf` to the latest available EEPROM image and uses `rpi-eeprom-update` to schedule an update when the system is rebooted.
```
sudo rpi-eeprom-config --apply boot.conf
sudo reboot
```

<a name="automaticupdates"></a>
## Automatic updates
The `rpi-eeprom-update` `systemd` service runs at startup and applies an update if a new image is available, automatically migrating the current bootloader configuration.

To disable automatic updates:  
```bash
sudo systemctl mask rpi-eeprom-update
```

To re-enable automatic updates:  
```bash
sudo systemctl unmask rpi-eeprom-update
```

#### Disabling automatic updates on multiple operating systems
If the [FREEZE_VERSION](bcm2711_bootloader_config.md#FREEZE_VERSION) bootloader EEPROM config is set then the EEPROM update service will skip any automatic updates. This removes the need to individually disable the EEPROM update service if there are multiple operating systems installed or when swapping SD-cards.

<a name="bootloader-release"></a>
## Bootloader release status
The firmware release status corresponds to a particular subdirectory of bootloader firmware images (`/lib/firmware/raspberrypi/bootloader/...`), and can be changed to select a different release stream.

* `default` - Updated for new hardware support, critical bug fixes and periodic update for new features that have been tested via the `latest` release.
* `latest` - Updated when new features have been successfully beta tested.
* `beta` - New or experimental features are tested here first.

Since the release status string is just a subdirectory name, then it is possible to create your own release streams e.g. a pinned release or custom network boot configuration.

N.B. `default` and `latest` are symbolic links to the older release names of `critical` and `stable`.

### Changing the bootloader release

You can change which release stream is to be used during an update by editing the `/etc/default/rpi-eeprom-update` file and changing the `FIRMWARE_RELEASE_STATUS` entry to the appropriate stream.

## Low level commands

## rpi-eeprom-update
Raspberry Pi OS uses the `rpi-eeprom-update` script to implement an [automatic update](#automaticupdates) service. The script can also be run interactively or wrapped to create a custom bootloader update service.

Reading the current EEPROM version:  
```bash
vcgencmd bootloader_version
```

Check if an update is available:  
```bash
sudo rpi-eeprom-update
```

Install the update:  
```
sudo rpi-eeprom-update -a
sudo reboot
```

Cancel the pending update:  
```bash
sudo rpi-eeprom-update -r
```

Installing a specific bootloader EEPROM image:  
```bash
sudo rpi-eeprom-update -d -f pieeprom.bin
```
The `-d` flag instructs `rpi-eeprom-update` to use the configuration in the specified image file instead of automatically migrating the current configuration.

Display the built-in documentation:  
```
rpi-eeprom-update -h
```

### Updating the bootloader configuration in an EEPROM image file
The following command replaces the bootloader configuration in `pieeprom.bin` with `boot.conf` and writes the new image to `new.bin`:
```bash
rpi-eeprom-config --config boot.conf --out new.bin pieeprom.bin
```

### recovery.bin
At power on, the BCM2711 ROM looks for a file called `recovery.bin` in the root directory of the boot partition on the SD card. If a valid `recovery.bin` is found then the ROM executes this instead of the SPI EEPROM image. This mechanism ensures that the bootloader SPI EEPROM can always be reset to a valid image with factory default settings.

See also [Raspberry Pi 4 boot-flow](bootmodes/bootflow_2711.md)

### EEPROM update files
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

For more information about the `rpi-eeprom-update` configuration file please run `rpi-eeprom-update -h`.

### EEPROM write protect
Both the bootloader and VLI SPI EEPROMs support hardware write-protection.  See the [eeprom_write_protect](bcm2711_bootloader_config.md#eeprom_write_protect) option for more information about how to enable this when flashing the EEPROMs.

## Release Notes
* [Release notes](https://github.com/raspberrypi/rpi-eeprom/blob/master/firmware/release-notes.md) for bootloader EEPROMs.
