# USB mass storage boot

**USB mass storage boot is available on Raspberry Pi 2B v1.2, 3A+, 3B, and 3B+ only. Support for USB mass storage boot will be added to the Raspberry Pi 4B in a future software update.**

This tutorial explains how to boot your Raspberry Pi from a USB mass storage device such as a flash drive or a USB hard disk. Note that this feature does not work with all USB mass storage devices.

## Program USB host boot mode (Raspberry Pi 3A+ and 3B only)

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

## Prepare the USB mass storage device

Copy a Raspbian or Raspbian Lite installation image directly onto your USB device, in the same way that you would for an SD card. To perform this step, follow the instructions [here](../../../installation/installing-images/README.md), remembering to select the drive that corresponds to your USB mass storage device. Make sure that you use a recent version of Raspbian/Raspbian Lite.

Once you have finished imaging your USB mass storage device, remove it from your computer and insert it into your Raspberry Pi.

## Boot your Raspberry Pi from the USB mass storage device

Attach the USB mass storage device to your Raspberry Pi, and power up the Pi. After five to ten seconds, the Raspberry Pi should begin booting and show the rainbow splash screen on an attached display. Make sure that you do not have an SD card inserted in the Pi, since if you do, it will boot from that first.
