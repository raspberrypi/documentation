# USB mass storage boot

**Available on Raspberry Pi 2B v1.2, 3A+, 3B, 3B+, 4B and 400 only.**

This page explains how to boot your Raspberry Pi from a USB mass storage device such as a flash drive or a USB hard disk. When attaching USB devices, particularly hard disks and SSDs, be mindful of their power requirements. If you wish to attach more than one SSD or hard disk to the Pi, this normally requires external power - either a powered hard disk enclosure, or a powered USB hub. Note that models prior to the Pi 4 have known issues which prevent booting with some USB devices.

See the [bootmodes documentation](README.md) for the boot sequence and alternative boot modes (network, USB device, GPIO or SD boot).

Note that 'USB mass storage boot' is different from 'USB device boot mode'. [USB device boot mode](device.md) allows a Raspberry Pi connected to a computer to boot as a USB device, using files from that computer.

If you are unable to use a particular USB device to boot your Raspberry Pi, an alternative for the Raspberry Pi 2B v1.2, 3A+, 3B, 3B+ models is to use the special bootcode.bin-only boot mode as described [here](README.md). This Pi will still boot from the SD card, but `bootcode.bin` is the only file read from it.

<a name="pi4"></a>
## Raspberry Pi 4B

To boot from a USB mass storage device, the Raspberry Pi 4B requires the bootloader EEPROM release from 3 September 2020 or later. Check which bootloader EEPROM version your Pi has using the `rpi-eeprom-update` tool:

```bash
pi@raspi4b:~ $ sudo rpi-eeprom-update
BCM2711 detected
Dedicated VL805 EEPROM detected
BOOTLOADER: up-to-date
CURRENT: Thu  3 Sep 12:11:43 UTC 2020 (1599135103)
 LATEST: Thu  3 Sep 12:11:43 UTC 2020 (1599135103)
 FW DIR: /lib/firmware/raspberrypi/bootloader/critical
VL805: up-to-date
CURRENT: 000138a1
 LATEST: 000138a1
 ```
 
The `rpi-eeprom-update` tool reports information about two different EEPROMs: the bootloader EEPROM and the VL805 USB controller EEPROM. The bootloader EEPROM information is reported after the `BOOTLOADER` heading: here the `CURRENT` release is what is installed in this Pi's EEPROM and is the 3 September 2020 release, so this Pi can do USB mass storage boot since it has the required version. The `LATEST` version shown is the most recent version available from the [APT](https://www.raspberrypi.org/documentation/linux/software/apt.md) package present on this Pi.
 
 If your Pi has an earlier release of bootloader EEPROM, there are two ways to upgrade to a version that can do USB mass storage boot:
 
 1. Use the `Misc Utility Images` option in the [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/) to create an SD card with the latest `Raspberry Pi 4 EEPROM boot recovery` image. Once you have imaged the SD card, boot the Pi with this card and a display connected to one (or both) of the HDMI ports. As the Pi boots, its bootloader EEPROM will be upgraded to the latest release. The display will turn green to indicate a successful update.
 1. Run Raspberry Pi OS 2020-08-20 or later from an SD card, and use it to upgrade the EEPROM. First, upgrade the packages on your system using the command `sudo apt update` followed by `sudo apt upgrade`. Once you have done this, run `sudo rpi-eeprom-update`: it will present a `LATEST` version of the bootloader EEPROM from 3 September 2020 or later. Once you can see this new EEPROM version in the output of `rpi-eeprom-update`, reboot the Pi to install it.
 
Once your Pi 4B has the 3 September 2020 or later bootloader EEPROM release, it can boot from a USB mass storage device. If an SD card is present, the Pi will attempt to boot from that first, before attempting boot from USB mass storage.

You can use the `raspi-config` tool to swap between SD/USB boot, and SD/network boot modes. The full set of boot mode options is documented on the [bootloader configuration](../bcm2711_bootloader_config.md) page.
 
<a name="pi400"></a>
## Raspberry Pi 400

All Raspberry Pi 400s have the bootloader EEPROM release from 3 September 2020 or later: there is no need to update the bootloader EEPROM to enable booting from USB mass storage. As with the Pi 4B, the Pi 400 will attempt to boot from the SD card first, before attempting boot from USB mass storage.

You can also use the `raspi-config` tool to swap between SD/USB boot, and SD/network boot modes. The full set of boot mode options is documented on the [bootloader configuration](../bcm2711_bootloader_config.md) page.


## Raspberry Pi 2B v1.2, 3A+, 3B, Compute Module 3

On the Raspberry Pi 2B v1.2, 3A+, 3B, and Compute Module 3 you must first enable [USB host boot mode](host.md). This is to allow USB mass storage boot, and [network boot](net.md). Note that network boot is not supported on the Raspberry Pi 3A+.

To enable USB host boot mode, the Raspberry Pi needs to be booted from an SD card with a special option to set the USB host boot mode bit in the one-time programmable (OTP) memory. Once this bit has been set, the SD card is no longer required. **Note that any change you make to the OTP is permanent and cannot be undone.**

**On the Raspberry Pi 3A+, setting the OTP bit to enable USB host boot mode will permanently prevent that Pi from booting in USB device mode.**

You can use any SD card running Raspberry Pi OS to program the OTP bit.

Enable USB host boot mode with this code:

```bash
echo program_usb_boot_mode=1 | sudo tee -a /boot/config.txt
```

This adds `program_usb_boot_mode=1` to the end of `/boot/config.txt`.

Note that although the option is named `program_usb_boot_mode`, it only enables USB *host* boot mode. USB *device* boot mode is only available on certain models of Raspberry Pi - see [USB device boot mode](device.md).

The next step is to reboot the Raspberry Pi with `sudo reboot` and check that the OTP has been programmed with:

```bash
$ vcgencmd otp_dump | grep 17:
17:3020000a
```

Check that the output `0x3020000a` is shown. If it is not, then the OTP bit has not been successfully programmed. In this case, go through the programming procedure again. If the bit is still not set, this may indicate a fault in the Pi hardware itself.

If you wish, you can remove the `program_usb_boot_mode` line from `config.txt`, so that if you put the SD card into another Raspberry Pi, it won't program USB host boot mode. Make sure there is no blank line at the end of `config.txt`.

You can now boot from a USB mass storage device in the same way as booting from an SD card - see the following section for further information.

## Raspberry Pi 3B+, Compute Module 3+

The Raspberry Pi 3B+ and Compute Module 3+ support USB mass storage boot out of the box. The steps specific to previous versions of Raspberry Pi do not have to be executed.

The [procedure](../../../installation/installing-images) is the same as for SD cards - simply image the USB storage device with the operating system image.

After preparing the storage device, connect the drive to the Raspberry Pi and power up the Pi, being aware of the extra USB power requirements of the external drive.
After five to ten seconds, the Raspberry Pi should begin booting and show the rainbow splash screen on an attached display. Make sure that you do not have an SD card inserted in the Pi, since if you do, it will boot from that first.

## Known issues (not Pi 4)

- The default timeout for checking bootable USB devices is 2 seconds. Some flash drives and hard disks power up too slowly. It is possible to extend this timeout to five seconds (add a new file `timeout` to the SD card), but note that some devices take even longer to respond.
- Some flash drives have a very specific protocol requirement that is not handled by the bootcode and may thus be incompatible.
