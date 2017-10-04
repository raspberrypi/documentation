# Raspberry Pi boot modes

## Introduction

The Raspberry Pi has a number of different stages of booting. This document is meant to help explain how the boot modes work, and which ones are supported for Linux booting.

* [Bootflow](bootflow.md): Boot sequence description
* [SD card](sdcard.md): SD card boot description
* [USB](usb.md): USB boot description
  * [Device boot](device.md): Booting as a mass storage device
  * [Host boot](host.md): Booting as a USB host
    * [Mass storage boot](msd.md): Boot from Mass Storage Device (MSD)
    * [Network boot](net.md): Boot from ethernet

## Special bootcode.bin-only boot mode

For the original Raspberry Pi and the Raspberry Pi 2 (based on the BCM2835 and BCM2836 devices), and in situations where the Pi 3 fails to boot, there is a new method of booting from one of the new boot modes (MSD or ethernet).

Just format an SD card as FAT32 and copy on the latest [bootcode.bin](https://github.com/raspberrypi/firmware/raw/master/boot/bootcode.bin). 

This will then enable the new bootmodes with some bug fixes for the failing Pi 3 cases.

If you have a problem with a mass storage device still not working even with this bootcode.bin, then please add a new file 'timeout' to the SD card. This should extend the time it waits for the mass storage device to initialise to six seconds.
