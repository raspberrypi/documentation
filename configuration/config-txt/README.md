# config.txt

The Raspberry Pi uses a configuration file instead of the [BIOS](https://en.wikipedia.org/wiki/BIOS) you would expect to find on a conventional PC. The system configuration parameters, which would traditionally be edited and stored using a BIOS, are stored instead in an optional text file named `config.txt`. This is read by the GPU before the ARM CPU and Linux are initialised. It must therefore be located on the first (boot) partition of your SD card, alongside `bootcode.bin` and `start.elf`. This file is normally accessible as `/boot/config.txt` from Linux, and must be edited as [root](../../linux/usage/root.md). From Windows or OS X it is visible as a file in the only accessible part of the card. If you need to apply some of the config settings below, but you don't have a `config.txt` on your boot partition yet, simply create it as a new text file.

Any changes will only take effect after you have rebooted your Raspberry Pi. After Linux has booted, you can view the current active settings using the following commands:

- `vcgencmd get_config <config>`: this displays a specific config value, e.g. `vcgencmd get_config arm_freq`.

- `vcgencmd get_config int`: this lists all the integer config options that are set (non-zero).

- `vcgencmd get_config str`: this lists all the string config options that are set (non-null).

Note that there are a few config settings that cannot be retrieved using `vcgencmd`.

## File format

The `config.txt` file is read by the early-stage boot firmware, so it has a very simple file format. The format is a single `property=value` statement on each line, where `value` is either an integer or a string. Comments may be added, or existing config values may be commented out and disabled, by starting a line with the `#` character.

There is an 80 character line length limit to entries, any characters past this limit will be ignored.

Here is an example file:

```
# Force the monitor to HDMI mode so that sound will be sent over HDMI cable
hdmi_drive=2
# Set monitor mode to DMT
hdmi_group=2
# Set monitor resolution to 1024x768 XGA 60Hz (HDMI_DMT_XGA_60)
hdmi_mode=16
# Make display smaller to stop text spilling off the screen
overscan_left=20
overscan_right=12
overscan_top=10
overscan_bottom=10
```

## config.txt Options

A range of options can be specified using the config.txt file. These are split into different sections, indexed below:

- [Memory](memory.md)
- [Licence Keys/Codecs](codeclicence.md)
- [Video/Display](video.md)
- [Audio](audio.md)
- [Camera](camera.md)
- [Boot](boot.md)
- [Ports and Device Tree](../device-tree.md#part4.6)
- [GPIOs](gpio.md)
- [Overclocking](overclocking.md)
- [Conditional Filters](conditional.md)
- [Miscellaneous](misc.md)




*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
