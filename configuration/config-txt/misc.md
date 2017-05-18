## Miscellaneous config.txt options

### avoid_warnings

The [warning symbols](../warning-icons.md) can be disabled using this option, although this is not advised.

`avoid_warnings=1` disables the warning overlays.
`avoid_warnings=2` disables the warning overlays, but additionally allows turbo mode even when low-voltage is present.

### logging_level

Sets the Videocore logging level. The value is a Videocore-specific bitmask.

### arm_64bit

If set, this forces the kernel loading system to assume a 64-bit kernel.
