# Miscellaneous options in config.txt

## avoid_warnings

The [warning symbols](../warning-icons.md) can be disabled using this option, although this is not advised.

`avoid_warnings=1` disables the warning overlays.
`avoid_warnings=2` disables the warning overlays, but additionally allows turbo mode even when low-voltage is present.

## logging_level

Sets the Videocore logging level. The value is a Videocore-specific bitmask.

## arm_control

Sets board-specific control bits. **NOTE:** This option is deprecated in favour of using the `arm_64bit` command to set the 64-bit boot control bit (arm_control=`0x200`).

## arm_64bit

If set, this forces the kernel loading system to assume a 64-bit kernel.

## include

Causes the content of the specified file to be inserted into the current file.

For example, adding the line `include extraconfig.txt` to `config.txt` will include the content of `extraconfig.txt` file in the `config.txt` file.
