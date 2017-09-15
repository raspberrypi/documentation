# How to boot from a USB Mass Storage Device on a Raspberry Pi 3

This tutorial explains how to boot your Raspberry Pi 3 from a USB mass storage device such as a flash drive or USB hard disk. Be warned that this feature is experimental and does not work with all USB mass storage devices. See [this blog post](https://www.raspberrypi.org/blog/pi-3-booting-part-i-usb-mass-storage-boot/) from Gordon Hollingworth for an explanation of why some USB mass storage devices don't work, as well as some background information.

## Program USB Boot Mode

Before a Raspberry Pi 3 will boot from a mass storage device, it needs to be booted from an SD card with a config option to enable USB boot mode. This will set a bit in the OTP (One Time Programmable) memory in the Raspberry Pi SoC that will enable booting from a USB mass storage device. Once this bit has been set, the SD card is no longer required. Note that any change you make to the OTP is permanent and cannot be undone.

You can use any SD card running Raspbian or Raspbian Lite to program the OTP bit. If you don't have such an SD card then you can install Raspbian or Raspbian Lite in the normal way - see [installing images](../../../installation/installing-images/README.md).

First, prepare the `/boot` directory with up to date boot files:

```bash
$ sudo apt-get update && sudo apt-get upgrade
```

The above step is not required if you use the 2017-04-10 release of Raspbian / Raspbian Lite or later.

Then enable USB boot mode with this code:

```bash
echo program_usb_boot_mode=1 | sudo tee -a /boot/config.txt
```

This adds `program_usb_boot_mode=1` to the end of `/boot/config.txt`. Reboot the Raspberry Pi with `sudo reboot`, then check that the OTP has been programmed with:

```bash
$ vcgencmd otp_dump | grep 17:
17:3020000a
```

Ensure the output `0x3020000a` is shown. If it is not, then the OTP bit has not been successfully programmed.

If you wish, you can remove the `program_usb_boot_mode` line from config.txt, so that if you put the SD card in another Raspberry Pi, it won't program USB boot mode. Make sure there is no blank line at the end of config.txt. You can edit config.txt using the nano editor using the command `sudo nano /boot/config.txt`, for example.

## Prepare the USB mass storage device
Starting with the 2017-04-10 release of Raspbian you can install a working Raspbian system to a USB mass storage device by copying the operating system image directly onto your USB device, in the same way that you would for an SD card. To perform this step, follow the instructions [here](../../../installation/installing-images/README.md), remembering to select the drive that corresponds to your USB mass storage device.

Once you have finished imaging your USB mass storage device, remove it from your computer and insert it into your Raspberry Pi 3.

## Boot your Raspberry Pi 3 from the USB mass storage device

Attach the USB mass storage device to your Raspberry Pi 3 and power it up. After between five and ten seconds the Raspberry Pi 3 should begin booting, and display the rainbow splash screen on an attached screen.
