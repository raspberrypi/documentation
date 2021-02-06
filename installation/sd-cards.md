# SD cards

Raspberry Pi computers use a micro SD card, except for very early models which use a full-sized SD card.

## Using very large SD cards on Raspberry Pi Zero, 1 and 2 computers

All Raspberry Pi computers can be used with a very large capacity - greater than 256GB. There is however a limitation which you may encounter if you use NOOBS on these devices.

There is a hardware limitation on Pi Zero, 1 and 2 computers which means that the boot partition must be 256GB or less, otherwise the Pi will not boot. Most operating systems use a small boot partition so this is not normally a problem. However, when using NOOBS, you will normally start by formatting the SD card as a single FAT32 partition which takes up the whole SD card. On SD cards larger than 256GB this will result in the Pi being unable to boot. This problem can be avoided by simply not using NOOBS; alternatively, create the FAT32 partition so that it has a size of 256GB or less.
