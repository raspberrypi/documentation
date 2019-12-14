# USB mass storage boot

**USB mass storage boot is available on Raspberry Pi 2B v1.2, 3A+, 3B, and 3B+ only. Support for USB mass storage boot will be added to the Raspberry Pi 4B in a future software update.**

This tutorial explains how to boot your Raspberry Pi from a USB mass storage device such as a flash drive or a USB hard disk. Note that this feature does not work with all USB mass storage devices.

See the [documentation](./) for the boot sequence and alternative boot modes (Network, USB device, GPIO or SD boot).

Note that "USB Mass Storage Boot" is different from "USB Device Boot Mode", the device boot mode allows a Raspberry Pi connected to a computer to boot using files on that computer.

## Raspberry Pi 1, 2 (V1.1), Compute Module, Zero

**These models are not supported for USB Mass Storage Boot.**
The boot code for USB is stored in the BCM2837 device only, so the Pi 1 A/B, Pi 2 B (v1.1), and Pi Zero will all require SD cards as they are based on the BCM2835 and BCM2836. This boot code is stored in ROM (except Pi 4B) which by definition cannot be changed.

An alternative is to use the 'special bootcode.bin-only boot mode' as described [here](./). This still requires/boots from an SD-card but allows to run on an USB Device.

## Raspberry Pi 2B v1.2, 3A+, 3B

On the Raspberry Pi 2B v1.2, 3A+, 3B, first USB [host boot mode](host.md) should be enabled. This is to allow Mass Storage Boot / Network boot (Network boot not supported on 3A+).

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

You can now boot from an USB Mass Storage device in the same way as booting from SD, see the following paragraph for Raspberry Pi 3B+.

## Raspberry Pi 3B+

The Raspberry Pi 3B+ supports USB Mass Storage boot out of the box. The settings specific to the previous versions of Raspberry Pi do not have to be executed.

This is verified using the following steps, this is the same (procedure)[../../../installation/installing-images/] as for SD cards though many alternative ways are functional:

1. Download Raspbian Buster Lite

2. Unzip the .zip file (tested with 7zip, but any other should be fine) to an .img file.

3. Initialise the drive (tested with MBR scheme, no partition/clean disk).

4. Flash the .img file to the external drive (tested using Win32DiskImager on Windows 10)

5. Unmount and disconnect the drive.

6. Connect the drive to the Raspberry Pi and power up the Pi (mind extra USB power usage from external drive).

7. After five to ten seconds, the Raspberry Pi should begin booting and show the rainbow splash screen on an attached display. Make sure that you do not have an SD card inserted in the Pi, since if you do, it will boot from that first.

## Raspberry Pi 4B

Support for USB mass storage boot will be added to the Raspberry Pi 4B in a future software update.

According to rpdom in a [forum post](https://www.raspberrypi.org/forums/viewtopic.php?t=243995#p1488036):

The Pi4 uses a different boot loader to the earlier models. It is stored in eeprom on the board instead of part in the chip and part on the SD card. An update and instructions on how to apply it will be issued when the USB and network boot is ready.

## Extra info

https://www.raspberrypi.org/blog/pi-3-booting-part-i-usb-mass-storage-boot/

## Known issues

- The default timeout for checking bootable USB devices is 2 seconds. Some flash drives and rotational harddrives power up too slowly. It’s possible to extend this timeout to five seconds (add a new file 'timeout'to the SD card), but there are devices that fail to respond within this period as well, such as the Verbatim PinStripe 64GB. 
- Some flash drives have a very specific protocol requirement that we don’t handle; as a result of this, we can’t talk to these drives correctly. An example of such a drive would be the Kingston Data Traveller 100 G3 32G.
- 3.5" HDD's commonly require 12V as well as 5V and commonly draw too much current for the Pi's USB connections.

## Known working devices

| Device Name                                       | Reported by |
|---|---|
| Sandisk Cruzer Fit 16GB                           | [Henry Budden](http://www.raspberrypitutorials.yolasite.com/) |
| Sandisk Cruzer Blade 16Gb                         | [Henry Budden](http://www.raspberrypitutorials.yolasite.com/) |
| Samsung 32GB USB 3.0 drive                        | [Henry Budden](http://www.raspberrypitutorials.yolasite.com/) |
| MeCo 16GB USB 3.0                                 | [Henry Budden](http://www.raspberrypitutorials.yolasite.com/) |
| Kingston A400 240GB (external 2.0 USB case MA6116) Raspbian Buster Lite | Paul-Ver | 
