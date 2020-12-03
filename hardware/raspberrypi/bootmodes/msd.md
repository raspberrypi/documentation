# USB mass storage boot

**Available on Raspberry Pi 2B v1.2, 3A+, 3B, 3B+, and 4B only.**

This page explains how to boot your Raspberry Pi from a USB mass storage device such as a flash drive or a USB hard disk. When attaching USB devices, particularly hard disks and SSDs, be mindful of their power requirements. If you wish to attach more than one SSD or hard disk to the Pi, this normally requires external power - either a powered hard disk enclosure, or a powered USB hub. Note that models prior to the Pi 4 have known issues which prevent booting with some USB devices.

See the [bootmodes documentation](README.md) for the boot sequence and alternative boot modes (network, USB device, GPIO or SD boot).

Note that 'USB mass storage boot' is different from 'USB device boot mode'. [USB device boot mode](device.md) allows a Raspberry Pi connected to a computer to boot as a USB device, using files from that computer.

If you are unable to use a particular USB device to boot your Raspberry Pi, an alternative is to use the special bootcode.bin-only boot mode as described [here](README.md). This Pi will still boot from the SD card, but `bootcode.bin` is the only file read from it.

<a name="pi4"></a>
## Raspberry Pi 4
To enable USB mass storage boot on a Raspberry Pi 4:

* Use the "Misc Utility Images" option in the [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/) to create a SD card with the latest "Raspberry Pi 4 EEPROM boot recovery" image.
* Update to Raspberry Pi OS 2020-08-20 or newer.
* Use [raspi-config](../../../configuration/raspi-config.md) to choose between SD/USB (default) or SD/Network boot modes.

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

The Raspberry Pi 3B+ and Compute Module 3+ support USB mass storage boot out of the box. The steps specific to previous versions of Raspberry Pi do not have to be executed.

The [procedure](../../../installation/installing-images) is the same as for SD cards - simply image the USB storage device with the operating system image.

After preparing the storage device, connect the drive to the Raspberry Pi and power up the Pi, being aware of the extra USB power requirements of the external drive.
After five to ten seconds, the Raspberry Pi should begin booting and show the rainbow splash screen on an attached display. Make sure that you do not have an SD card inserted in the Pi, since if you do, it will boot from that first.

## Known issues (not Pi 4)

- The default timeout for checking bootable USB devices is 2 seconds. Some flash drives and hard disks power up too slowly. It is possible to extend this timeout to five seconds (add a new file `timeout` to the SD card), but note that some devices take even longer to respond.
- Some flash drives have a very specific protocol requirement that is not handled by the bootcode and may thus be incompatible.
