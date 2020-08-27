# Miscellaneous options in config.txt

## avoid_warnings

The [warning symbols](../warning-icons.md) can be disabled using this option, although this is not advised.

`avoid_warnings=1` disables the warning overlays.
`avoid_warnings=2` disables the warning overlays, but additionally allows turbo mode even when low-voltage is present.

## logging_level

Sets the VideoCore logging level. The value is a VideoCore-specific bitmask.

## include

Causes the content of the specified file to be inserted into the current file.

For example, adding the line `include extraconfig.txt` to `config.txt` will include the content of `extraconfig.txt` file in the `config.txt` file.

**Include directives are not supported by bootcode.bin or the EEPROM bootloader**

## max_usb_current

**This command is now deprecated and has no effect.** Originally certain models of Raspberry Pi limited the USB ports to a maximum of 600mA. Setting `max_usb_current=1` changed this default to 1200mA. However, all firmware now has this flag set by default, so it is no longer necessary to use this option.
