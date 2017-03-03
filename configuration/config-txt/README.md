# config.txt

The Raspberry Pi doesn't have a [BIOS](https://en.wikipedia.org/wiki/BIOS) like you'd find on a conventional PC. This is because it is an embedded platform. The various system configuration parameters, which would traditionally be edited and stored using a BIOS, are stored in an optional text file named `config.txt`. This is read by the GPU before the ARM CPU and Linux are initialised; it must therefore be located on the first (boot) partition of your SD card, alongside `bootcode.bin` and `start.elf`. This file is normally accessible as `/boot/config.txt` from Linux and must be edited as [root](../linux/usage/root.md), but from Windows or OS X it is seen as a file in the only accessible part of the card. If you need to apply some of the config settings below, but you don't have a `config.txt` on your boot partition yet, then simply create it as a new text file.

Any changes will only take effect after you've rebooted your Raspberry Pi. After Linux has booted, you can get the current active settings with the following commands:

`vcgencmd get_config <config>` - displays a specific config value, e.g. `vcgencmd get_config arm_freq`.

`vcgencmd get_config int` - lists all the integer config options that are set (non-zero).

`vcgencmd get_config str` - lists all the string config options that are set (non-null).

Note that there are a few config settings which can't be retrieved using `vcgencmd`.

## File format

As `config.txt` is read by the early-stage boot firmware it has a very simple file format. The format is a single `property=value` statement on each line, where `value` is either an integer or a string. Comments may be added, or existing config values may be commented out and disabled, by starting a line with the `#` character.

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

# config.txt Options

There are a large number of options that can be put in the config.txt file. These are broken up in to different sections indexed below.

- [Memory](memory.md)
- [Licence Keys/Codecs](codeclicence.md)
- [Video/Display](video.md)
- [Audio](audio.md)
- [Camera](camera.md)
- [Boot](boot.md)
- [Device Tree](../device-tree.md)
- [Overclocking](overclocking.md)
- [Conditional Filters](conditional.md)





*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
