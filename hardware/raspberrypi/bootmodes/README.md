# Raspberry Pi boot modes

## Introduction

The Raspberry Pi has a number of different stages of booting. This document explains how the boot modes work, and which ones are supported for Linux booting.

[Boot Sequence](bootflow.md)

[SD card boot](sdcard.md)

[USB boot](usb.md) comprises the following two modes:
* [Device boot](device.md): booting as a mass storage device
* [Host boot](host.md): booting as a USB host using one of the following:
  * [Mass storage boot](msd.md): boot from mass storage device
  * [Network boot](net.md): boot via Ethernet
  
[GPIO boot mode](gpio.md)
  
## Special bootcode.bin-only boot mode
USB host and Ethernet boot can be performed by BCM2837-based Raspberry Pis - that is, Pi 2B version 1.2, Pi 3B, and Pi 3B+ (Raspberry Pi 3A+ cannot net boot since it does not have a built-in Ethernet interface). In addition, all Raspberry Pi models **except Pi 4B** can use a new bootcode.bin-only method to enable USB host boot.

**Note:** The Raspberry Pi 4B does not use the bootcode.bin file - instead the bootloader is located in an on-board EEPROM chip. The Pi 4B bootloader currently only supports booting from an SD card. Support for USB host mode boot and Ethernet boot will be added by a future software update. See [Pi4 Bootflow](./bootflow_2711.md) and  [SPI Boot EEPROM](../booteeprom.md).

Format an SD card as FAT32 and copy on the latest [bootcode.bin](https://github.com/raspberrypi/firmware/raw/master/boot/bootcode.bin). The SD card must be present in the Pi for it to boot. Once bootcode.bin is loaded from the SD card, the Pi continues booting using USB host mode.

This is useful for the Raspberry Pi 1, 2, and Zero models, which are based on the BCM2835 and BCM2836 chips, and in situations where a Pi 3 fails to boot (the latest bootcode.bin includes additional bugfixes for the Pi 3B, compared to the boot code burned into the BCM2837A0).

If you have a problem with a mass storage device still not working, even with this bootcode.bin, then please add a new file 'timeout' to the SD card. This will extend to six seconds the time for which it waits for the mass storage device to initialise.

## bootcode.bin UART enable (Pre Raspberry Pi 4B)

For information on enabling the UART on the Pi4 bootloader, please see [this page](../bcm2711_bootloader_config.md).

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
