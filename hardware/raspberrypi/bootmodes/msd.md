# How to boot from a USB mass storage device on a Raspberry Pi

**USB boot is available on the Raspberry Pi 3B, 3B+, 3A+ and Raspberry Pi 2B v1.2 models only.**

This tutorial explains how to boot your Raspberry Pi from a USB mass storage device such as a flash drive or USB hard disk. Be warned that this feature is experimental and does not work with all USB mass storage devices. See [this blog post](https://www.raspberrypi.org/blog/pi-3-booting-part-i-usb-mass-storage-boot/) from Gordon Hollingworth for an explanation of why some USB mass storage devices don't work, as well as for some background information.

## Program USB boot mode

The Raspberry Pi 3+ is able to boot from USB without any changes, but the Raspberry Pi 3 requires the USB boot bit to be set in the OTP (one-time programmable) memory. If you are using a Raspberry Pi 3+, please go to the next section.

To enable the USB boot bit, the Raspberry Pi 3 needs to be booted from an SD card with a `config` option to enable USB boot mode. 

Once this bit has been set, the SD card is no longer required. **Note that any change you make to the OTP is permanent and cannot be undone.**

You can use any SD card running Raspbian or Raspbian Lite to program the OTP bit. If you don't have such an SD card then you can install Raspbian or Raspbian Lite in the normal way - see [installing images](../../../installation/installing-images/README.md).

First, prepare the `/boot` directory with up to date boot files (this step is not required if you're using the 2017-04-10 release of Raspbian/Raspbian Lite or a later one):

```bash
$ sudo apt-get update && sudo apt-get upgrade
```

Then enable USB boot mode with this code:

```bash
echo program_usb_boot_mode=1 | sudo tee -a /boot/config.txt
```

This adds `program_usb_boot_mode=1` to the end of `/boot/config.txt`. Reboot the Raspberry Pi with `sudo reboot`, then check that the OTP has been programmed with:

```bash
$ vcgencmd otp_dump | grep 17:
17:3020000a
```

Check that the output `0x3020000a` is shown. If it is not, then the OTP bit has not been successfully programmed. In this case, go through the programming procedure again. If the bit is still not set, this may indicate a fault in the Pi hardware itself.

If you wish, you can remove the `program_usb_boot_mode` line from config.txt, so that if you put the SD card in another Raspberry Pi, it won't program USB boot mode. Make sure there is no blank line at the end of config.txt. You can edit config.txt using the nano editor using the command `sudo nano /boot/config.txt`, for example.

## Prepare the USB mass storage device

Starting with the 2017-04-10 release of Raspbian you can install a working Raspbian system to a USB mass storage device by copying the operating system image directly onto your USB device, in the same way that you would for an SD card. To perform this step, follow the instructions [here](../../../installation/installing-images/README.md), remembering to select the drive that corresponds to your USB mass storage device.

Once you have finished imaging your USB mass storage device, remove it from your computer and insert it into your Raspberry Pi.

## Boot your Raspberry Pi from the USB mass storage device

Attach the USB mass storage device to your Raspberry Pi, and power the Pi up. After five to ten seconds, the Raspberry Pi should begin booting and show the rainbow splash screen on an attached display.

Note that if the USB boot bit is set, you do not need to insert an SD card into the Raspberry Pi for USB boot to work.
