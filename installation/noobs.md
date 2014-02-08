# NOOBS

**New Out Of the Box Software** - an easy Operating System install manager for the Raspberry Pi

## How to get NOOBS

### Buy a preinstalled SD card

The easiest way to get NOOBS is to buy an SD card with NOOBS preinstalled - available for £4 on the swag store.

### Download

Alternatively, NOOBS is available for download on the Raspberry Pi website: [http://downloads.raspberrypi.org/NOOBS_latest]

#### How to install NOOBS on an SD card

Once you've downloaded the NOOBS zip file, you'll need to copy the contents to a fomatted SD card on your computer.

To setup a blank SD card with NOOBS:

- Format an SD card that is 4GB or greater in size as FAT (see instructions on how to do this below)

- Download and extract the files from the NOOBS zip file

- Copy the extracted files onto the SD card that you just formatted so that this file is at the root directory of the SD card. Please note that in some cases it may extract the files into a folder, if this is the case then please copy across the files from inside the folder rather than the folder itself.

- On first boot the "RECOVERY" FAT partition will be automatically resized to a minimum and a list of OSes that are available to install will be displayed.

#### How to Format an SD card as FAT

##### Windows

For Windows users, we recommend formatting your SD card using the SD Association's Formatting Tool, which can be downloaded from [sdcard.org](https://www.sdcard.org/downloads/formatter_4/). You will need to set "FORMAT SIZE ADJUSTMENT" option to "ON" in the "Options" menu to ensure that the entire SD card volume is formatted - not just a single partition.

##### Mac OS

The SD Association's Formatting Tool is also available for Mac users although the default OSX Disk Utility is also capable of formatting the entire disk (select the SD card volume and choose "Erase" with "MS-DOS" format).

##### Linux

For Linux users we recommend ```gparted``` (or the command line version ```parted```). Norman Dunbar has written up [instructions](http://qdosmsq.dunbar-it.co.uk/blog/2013/06/noobs-for-raspberry-pi/) for Linux users.

## What's included in NOOBS

The following Operating Systems are currently included in NOOBS:

- Raspbian

- OpenELEC

- RISC OS

- Arch Linux

- RaspBMC

- Pidora

## NOOBS and NOOBS Lite

NOOBS is available in two forms: offline and network install or network install only.

The full version has the images of each of the Operating Systems included, so they can be installed from the SD card while offline, whereas NOOBS Lite requires an internet connection to download the selected Operating System.

Note that the Operating System images on the full version can be outdated if a new version of the OS is released, but if connected to the internet you will be shown the option of downloading the new version of the OS if there is a newer one available.

## NOOBS Development

### Latest NOOBS release

The latest NOOBS release is **v1.3.4**, released on **9th January 2014***

### NOOBS Documentation

A more comprehensive documentation including more avdanced configuration of NOOBS is available on [GitHub](https://github.com/raspberrypi/noobs/README.md)

### NOOBS source code

See the NOOBS source code on [GitHub](https://github.com/raspberrypi/noobs)