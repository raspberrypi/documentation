# Raspberry Pi boot modes

## Introduction

The Raspberry Pi has a number of different stages of booting. This document is meant to help explain how the boot modes work, and which ones are supported for Linux booting.

* [Bootflow](./bootflow): Boot sequence description
* [SD card](./sdcard): SD card boot description
* [USB](./usb): USB boot description
  * [Device boot](./device): Booting as a mass storage device
  * [Host boot](./host): Booting as a USB host
    * [Mass storage boot](./msd): Boot from Mass Storage Device (MSD)
    * [Network boot](./net): Boot from ethernet

## Special bootcode.bin-only boot mode

For the original Raspberry Pi and the Raspberry Pi 2 (based on the BCM2835 and BCM2836 devices), and in situations where the Pi 3 fails to boot, there is a new method of booting from one of the new boot modes (MSD or ethernet).

Just format an SD card as FAT32 and copy on the latest [bootcode.bin](https://github.com/raspberrypi/firmware/raw/master/boot/bootcode.bin).

This will then enable the new bootmodes with some bug fixes for the failing Pi 3 cases.

If you have a problem with a mass storage device still not working even with this bootcode.bin, then please add a new file 'timeout' to the SD card. This should extend the time it waits for the mass storage device to initialise to six seconds.

## bootcode.bin UART enable

It is possible to enable an early stage UART to debug booting issues (useful with the above bootcode.bin only boot mode).  To do this, make sure you've got a recent version of the firmware (including bootcode.bin).  To check if UART is supported in your current firmware:

```
$ strings bootcode.bin | grep BOOT_UART
BOOT_UART=0
```

To enable UART from bootcode.bin use:

```
sed -i -e "s/BOOT_UART=0/BOOT_UART=1/" bootcode.bin
```

Next, connect a suitable USB serial cable to your host computer (a Raspberry Pi will work, although I find the easiest path is to use a USB serial cable since it'll work out the box without any pesky config.txt settings).  Use the standard pins 6, 8 and 10 (GND, GPIO14, GPIO15) on a Pi or CM board.

Then use `screen` on linux or a Mac or `putty` on windows to connect to the serial.

Setup your serial to receive at 115200-8-N-1, and then boot your Pi / Compute module.  You should get an immediate serial output from the device as bootcode.bin runs.
