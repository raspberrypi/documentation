# USB mass storage boot

**USB mass storage boot is available on Raspberry Pi 2B v1.2, 3A+, 3B, and 3B+ only. Support for USB mass storage boot will be added to the Raspberry Pi 4B in a future software update.**

This page explains how to boot your Raspberry Pi from a USB mass storage device such as a flash drive or a USB hard disk. Note that this feature does not work with all USB mass storage devices.

See the [bootmodes documentation](README.md) for the boot sequence and alternative boot modes (Network, USB device, GPIO or SD boot).

Note that "USB mass storage boot" is different from "USB device boot mode". The [device boot mode](device.md) allows a Raspberry Pi connected to a computer to boot using files on that computer.

For devices that are not supported, an alternative is to use the 'special bootcode.bin-only boot mode' as described [here](README.md). This still requires/boots from an SD-card, but `bootcode.bin` is the only file read from the SD-Card.

## Raspberry Pi 2B v1.2, 3A+, 3B, CM3

On the Raspberry Pi 2B v1.2, 3A+, 3B, CM3, first USB [host boot mode](host.md) should be enabled. This is to allow "mass storage boot" and ["network boot"](net.md) (Network boot not supported on 3A+).

To enable USB host boot mode, the Raspberry Pi needs to be booted from an SD card with a special option to set the USB host boot mode bit in the OTP (one-time programmable) memory. 

Once this bit has been set, the SD card is no longer required. **Note that any change you make to the OTP is permanent and cannot be undone.**

**On the Raspberry Pi 3A+, setting the OTP bit to enable USB host boot mode will permanently prevent that Pi from booting in USB device mode.**

You can use any SD card running Raspbian or Raspbian Lite to program the OTP bit.

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

If you wish, you can remove the `program_usb_boot_mode` line from config.txt, so that if you put the SD card into another Raspberry Pi, it won't program USB host boot mode. Make sure there is no blank line at the end of config.txt.

You can now boot from an USB mass storage device in the same way as booting from SD, see the following paragraph for Raspberry Pi 3B+, CM3+.

## Raspberry Pi 3B+, CM3+

The Raspberry Pi 3B+ and CM3+ support USB mass storage boot out of the box. The settings specific to the previous versions of Raspberry Pi do not have to be executed.

This is the same [procedure](../../../installation/installing-images) as for SD cards.

After preparing the storage device, connect the drive to the Raspberry Pi and power up the Pi (be aware of the extra USB power usage from the external drive).
After five to ten seconds, the Raspberry Pi should begin booting and show the rainbow splash screen on an attached display. Make sure that you do not have an SD card inserted in the Pi, since if you do, it will boot from that first.

<a name="pi4"></a>
## Raspberry Pi 4

The Raspberry Pi 4's bootcode is stored in [EEPROM](../booteeprom.md) and can be updated. Support for mass storage boot will be added in a future update.

## Known issues

- The default timeout for checking bootable USB devices is 2 seconds. Some flash drives and rotational harddrives power up too slowly. It’s possible to extend this timeout to five seconds (add a new file `timeout` to the SD card), but there are devices that fail to respond within this period as well.
- Some flash drives have a very specific protocol requirement that is not handled by the bootcode and may thus be incompatible.
- Lack of power can be an issue, so it is recommended to use a powered USB hub, particularly if you are attaching more than one storage device to the Raspberry Pi. If your device has its own power supply, then use that.
