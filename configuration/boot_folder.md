# The boot folder

In a basic Raspbian install, the boot files are stored on the first partition of the SD card, which is formatted with the FAT file system. This means that it can be read on Windows, macOS, and Linux devices.

When the Raspberry Pi is powered on, it loads various files from the boot partition/folder in order to start up the various processors, then it boots the Linux kernel.

Once Linux has booted, the boot partition is mounted as `/boot`.

## Boot folder contents

### bootcode.bin

This is the bootloader, which is loaded by the SoC on boot, does some very basic setup, and then loads one of the `start*.elf` files. `bootcode.bin` is not used on the Raspberry Pi 4, because it has been replaced by boot code in the [onboard EEPROM](../hardware/raspberrypi/booteeprom.md).

### start.elf, start_x.elf, start_db.elf, start_cd.elf, start4.elf, start4x.elf, start4cd.elf, start4db.elf

These are binary blobs (firmware) that are loaded on to the VideoCore in the SoC, which then take over the boot process.
`start.elf` is the basic firmware, `start_x.elf` includes camera drivers and codec, `start_db.elf` is a debug version of the firmware, and `start_cd.elf` is a cut-down version with no support hardware blocks like codecs and 3D, and for use when `gpu_mem=16` is specified in `config.txt`. More information on how to use these can be found in [the `config.txt` section](./config-txt/boot.md).

`start4.elf`, `start4x.elf`, `start4cd.elf`, and `start4db.elf` are firmware files specific to the Pi 4.

### fixup*.dat

These are linker files and are matched pairs with the `start*.elf` files listed in the previous section.

### cmdline.txt

The kernel command line passed in to the kernel when it boots.

### config.txt

Contains many configuration parameters for setting up the Pi. See [the `config.txt` section](./config-txt/README.md).

### issue.txt

Some text-based housekeeping information containing the date and git commit ID of the distribution.

### Device Tree files

There are various Device Tree blob files, which have the extension `.dtb`. These contain the hardware definitions of the various models of Raspberry Pi, and are used on boot to set up the kernel according to which Pi model is detected. More [details here](device-tree.md).

## Device Tree overlays

The `overlays` sub-folder contains Device Tree overlays. These are used to configure various hardware devices that may be attached to the system, for example the Raspberry Pi Touch Display or third-party sound boards. These overlays are selected using entries in `config.txt` — see ['Device Trees, overlays and parameters, part 2' for more info](device-tree.md#part2).
