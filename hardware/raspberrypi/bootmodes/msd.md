# USB mass storage boot

**Available on Raspberry Pi 2B v1.2, 3A+, 3B, 3B+, 4B, 400, Compute Module 3, Compute Module 3+ and Compute Module 4 only.**

This page explains how to boot your Raspberry Pi from a USB mass storage device such as a flash drive or a USB hard disk. When attaching USB devices, particularly hard disks and SSDs, be mindful of their power requirements. If you wish to attach more than one SSD or hard disk to the Pi, this normally requires external power - either a powered hard disk enclosure, or a powered USB hub. Note that models prior to the Pi 4B have known issues which prevent booting with some USB devices.

<a name="pi400"></a>
## Raspberry Pi 400
To boot the Pi 400 from a USB mass storage device, simply image the USB drive with Raspberry Pi OS 2020-08-20 or newer using the Raspberry Pi Imager utility: select the USB drive from the `SD Card` list in Raspberry Pi Imager.

<a name="pi4"></a>
## Raspberry Pi 4B
Depending on when your Raspberry Pi 4B was manufactured, the bootloader EEPROM may need to be updated to enable booting from USB mass storage devices. 

### Check if your Pi 4B has the required bootloader EEPROM version

To check if your Pi 4B has the required bootloader EEPROM version, power it up with with no SD card inserted and a display attached to one of the HDMI ports. The Pi 4B will display a diagnostic screen on the attached display, which includes the bootloader EEPROM version at the top of the screen. The bootloader must be dated `Sep 3 2020` or later to support USB mass storage boot. If the diagnostic screen reports a date earlier than `Sep 3 2020`, or there is no diagnostic screen shown, you will need to update the bootloader EEPROM first to enable USB mass storage boot.

USB mass storage boot on the Pi 4B requires Raspberry Pi OS 2020-08-20 or later.


### Enable USB mass storage boot on a Pi 4B by updating the bootloader EEPROM
If your Pi 4B requires an updated bootloader EEPROM in order to support USB mass storage boot, you can perform the update as follows:

1. Use the "Misc Utility Images" option in [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/) to create an SD card with the latest "Raspberry Pi 4 EEPROM boot recovery" image.
1. Boot the Pi 4B using this SD card.
1. The bootloader EEPROM will be updated to the latest factory version, then the Pi will flash its green ACT light rapidly, and display green on the HDMI outputs to indicate success.

The Pi 4B can now be booted from a USB mass storage device.

## Changing boot order on Pi 4B and Pi 400

The [raspi-config](../../../configuration/raspi-config.md) utility can be used to choose between SD/USB (default) or SD/Network boot modes.

The full set of boot mode options is documented on the [bootloader configuration](../bcm2711_bootloader_config.md) page.


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

The Raspberry Pi 3B+ and Compute Module 3+ support USB mass storage boot out of the box: no changes to the OTP memory are required.

The [procedure](../../../installation/installing-images) is the same as for SD cards - simply image the USB storage device with the operating system image.

After preparing the storage device, connect the drive to the Raspberry Pi and power up the Pi, being aware of the extra USB power requirements of the external drive.
After five to ten seconds, the Raspberry Pi should begin booting and show the rainbow splash screen on an attached display. Make sure that you do not have an SD card inserted in the Pi, since if you do, it will boot from that first.

See the [bootmodes documentation](README.md) for the boot sequence and alternative boot modes (network, USB device, GPIO or SD boot).

## Known issues (not Pi 4B, CM4 and Pi 400)

- The default timeout for checking bootable USB devices is 2 seconds. Some flash drives and hard disks power up too slowly. It is possible to extend this timeout to five seconds (add a new file `timeout` to the SD card), but note that some devices take even longer to respond.
- Some flash drives have a very specific protocol requirement that is not handled by the bootcode and may thus be incompatible.

## Special bootcode.bin-only boot mode (not Pi 4B, CM4 and Pi 400)
If you are unable to use a particular USB device to boot your Raspberry Pi, an alternative for the Pi 2B v1.2, 3A+, 3B and 3B+ is to use the special bootcode.bin-only boot mode as described [here](README.md). The Pi will still boot from the SD card, but `bootcode.bin` is the only file read from it.
