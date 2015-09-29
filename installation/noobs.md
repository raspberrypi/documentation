# NOOBS

**New Out Of the Box Software** - an easy operating system install manager for the Raspberry Pi

![NOOBS OS selection](images/noobs.png)

## How to get NOOBS

### Buy a pre-installed SD card

The easiest way to get NOOBS is to buy an SD card with NOOBS pre-installed; this is available for £4 on the [swag store](http://swag.raspberrypi.org/collections/frontpage/products/noobs-8gb-sd-card).

### Download

Alternatively, NOOBS is available for download on the Raspberry Pi website: [raspberrypi.org/downloads](http://www.raspberrypi.org/downloads)

#### How to install NOOBS on an SD card

Once you've downloaded the NOOBS zip file, you'll need to copy the contents to a formatted SD card on your computer.

To set up a blank SD card with NOOBS:

- Format an SD card that is 4GB or larger as FAT. See instructions on how to do this below.
- Download and extract the files from the NOOBS zip file.
- Copy the extracted files onto the SD card that you just formatted so that this file is at the root directory of the SD card. Please note that in some cases it may extract the files into a folder; if this is the case then please copy across the files from inside the folder rather than the folder itself.
- On first boot the "RECOVERY" FAT partition will be automatically resized to a minimum, and a list of OSs that are available to install will be displayed.

#### How to format an SD card as FAT

**Note:** If you're formatting an SD (or micro SD) card that has a capacity over 32 GB (i.e. 64GB and above) then see the separate [SDXC formatting](sdxc_formatting.md) instructions.

##### Windows

For Windows users we recommend formatting your SD card using the SD Association's Formatting Tool, which can be downloaded from [sdcard.org](https://www.sdcard.org/downloads/formatter_4/). You will need to set "FORMAT SIZE ADJUSTMENT" option to "ON" in the "Options" menu to ensure that the entire SD card volume is formatted, and not just a single partition.

##### Mac OS

The [SD Association's Formatting Tool](https://www.sdcard.org/downloads/formatter_4/) is also available for Mac users, although the default OSX Disk Utility is also capable of formatting the entire disk. To do this, select the SD card volume and choose `Erase` with `MS-DOS` format.

##### Linux

For Linux users we recommend `gparted` (or the command line version `parted`). Norman Dunbar has written up [instructions](http://qdosmsq.dunbar-it.co.uk/blog/2013/06/noobs-for-raspberry-pi/) for Linux users.

## What's included in NOOBS

The following Operating Systems are currently included in NOOBS:

- [Raspbian](http://raspbian.org/)
- [Pidora](http://pidora.ca/)
- [OpenELEC](http://wiki.openelec.tv/index.php?title=Raspberry_Pi_FAQ)
- [OSMC](http://osmc.tv/)
- [RISC OS](https://www.riscosopen.org/wiki/documentation/show/Welcome%20to%20RISC%20OS%20Pi)
- [Arch Linux](http://archlinuxarm.org/platforms/armv6/raspberry-pi)

As of NOOBS v1.3.10 (September 2014), only Raspbian is installed by default in NOOBS. The others can be installed with a network connection.

## NOOBS and NOOBS Lite

NOOBS is available in two forms: offline and network install; or network install only.

The full version has Raspbian included, so it can be installed from the SD card while offline, whereas using NOOBS Lite,  or installing any other operating system, requires an internet connection during installation.

Note that the operating system image on the full version can be outdated if a new version of the OS is released, but if connected to the internet you will be shown the option of downloading the latest version if there is a newer one available.

## NOOBS Development

### Latest NOOBS release

The latest NOOBS release is **v1.4.2**, released on **28th September 2015**.

(From NOOBS v1.4.0 onwards, NOOBS Lite only shares the first two digits of the version number, i.e. v1.4)

### NOOBS Documentation

A more comprehensive documentation, including more advanced configuration of NOOBS, is available on [GitHub](https://github.com/raspberrypi/noobs/blob/master/README.md).

### NOOBS source code

See the NOOBS source code on [GitHub](https://github.com/raspberrypi/noobs).
