# The Boot folder

In a basic Raspbian install, the boot files are stored on the first partition of the SD card, which is VFAT-formatted. This means that it can be read on both Windows and Linux devices. 

When the Raspberry Pi is powered on, it loads various files from the boot partition/folder in order to start up the various processors, then it boots the Linux kernel.

## Boot folder contents

### bootcode.bin

The bootloader. Loaded by the SoC on boot, does some very basic setup, and subsequently loads one of the `start*.elf` files.

### start.elf, start_x.elf, start_db.elf, start_cd.elf

These are binary blobs (firmware) that are loaded on to the VideoCore in the SoC, which then take over the boot process.
`start.elf` is the basic firmware, `start_x.elf` includes camera drivers and codec, `start_db.elf` is a debug version of the firmware, and `start_cd.elf` is a cut-down version with no support hardware blocks like codecs and 3D, and for use when `gpu_mem=16` is specified in `config.txt`. More information on how to use these can be found in [the `config.txt` section](./config-txt/boot.md).

### fixup.dat, fixup_x.dat, fixup_db.dat, fixup_cd.dat

These are linker files and are matched pairs with the `start*.elf` files.

### cmdline.txt

The kernel command line passed in to the kernel when it boots.

### config.txt

Contains many configuration parameters for setting up the Pi. See [the `config.txt` section](./config-txt/README.md).

### issue.txt

Some text-based housekeeping information containing the date and git commit ID of the distribution.

### Device Tree files

There are various Device Tree blob files, `\*.dtb`. These contain the hardware definitions of the various Pi models, and are used on boot to set up the kernel according to which Pi model is detected. More [details here](device-tree.md).
