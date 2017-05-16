# Formatting an SDXC card for use with NOOBS

According to the [SD specifications](https://www.sdcard.org/developers/overview/capacity/), any SD card larger than 32GB is an SDXC card and has to be formatted with the exFAT filesystem. This means the official SD Formatter tool will *always* format cards that are 64GB or larger as exFAT.

The Raspberry Pi's bootloader, built into the GPU and non-updateable, only has support for reading from FAT filesystems (both FAT16 and FAT32), and is unable to boot from an exFAT filesystem. So if you want to use NOOBS on a card that is 64GB or larger, you need to reformat it as FAT32 first before copying the NOOBS files to it.

## Linux and Mac OS

The standard formatting tools built into these operating systems are able to create FAT32 partitions; they might also be labelled as FAT or MS-DOS. Simply delete the existing exFAT partition and create and format a new FAT32 primary partition, before proceeding with the rest of the [NOOBS instructions](noobs.md).

### Mac OS CLI

Create one 30GB FAT32 partition. NOOBS will resize to the full size of the SD card during installation.

1. Plug SD card into computer
1. Open terminal application
1. ```sudo diskutil list```
   1. Find your card, i.e. /dev/disk2
1. ```sudo diskutil eraseDisk FAT32 NOOBS MBR <device>```
1. ```sudo diskutil splitPartition <device>s1 2 FAT32 NOOBS1 30G FAT32 TMP 1G```

## Windows

The standard formatting tools built into Windows are limited, as they only allow partitions up to 32GB to be formatted as FAT32, so to format a 64GB partition as FAT32 you need to use a third-party formatting tool. A simple tool to do this is [FAT32 Format](http://www.ridgecrop.demon.co.uk/guiformat.htm) which downloads as a single file named `guiformat.exe` - no installation is necessary.

Run the [SD Formatter](https://www.sdcard.org/downloads/formatter_4/) tool first with "FORMAT SIZE ADJUSTMENT" set to "ON", to ensure that any other partitions on the SD card are deleted. Then run the FAT32 Format (guiformat.exe) tool, ensure you choose the correct drive letter, leave the other options at their default settings, and click "Start". After it has finished, you can proceed with the rest of the [NOOBS instructions](noobs.md).

If the FAT32 Format tool doesn't work for you, alternative options are [MiniTool Partition Wizard Free Edition](http://www.minitool.com/partition-manager/partition-wizard-home.html) and [EaseUS Partition Master Free](http://www.easeus.com/partition-manager/epm-free.html) which are "home user" versions of fully featured partition editor tools, and so not as straightforward to use.
