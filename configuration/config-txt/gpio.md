# GPIO control in config.txt

## `gpio`
The `gpio` directive allows GPIO pins to be set to specific modes and values at boot time in a way that would
previously have needed a custom `dt-blob.bin` file. Each line applies the same settings (or at least makes the same
changes) to a set of pins, either a single pin (`3`), a range of pins (`3-4`), or a comma-separated list of either (`3-4,6,8`).
The pin set is followed by an `=` and one or more comma-separated attributes from this list:

* `ip` - Input
* `op` - Output
* `a0-a5` - Alt0-Alt5
* `dh` - Driving high (for outputs)
* `dl` - Driving low (for outputs)
* `pu` - Pull up
* `pd` - Pull down
* `pn/np` - No pull

`gpio` settings are applied in order, so those appearing later override those appearing earlier.

Examples:
```
# Select Alt2 for GPIO pins 0 to 27 (for DPI24)
gpio=0-27=a2

# Set GPIO12 to be an output set to 1
gpio=12=op,dh

# Change the pull on (input) pins 18 and 20
gpio=18,20=pu

# Make pins 17 to 21 inputs
gpio=17-21=ip
```

The `gpio` directive respects the "[...]" section headers in `config.txt`, so it is possible to use different settings
based on the model, serial number, and EDID.

GPIO changes made through this mechanism do not have any direct effect on the kernel — they don't cause GPIO pins to
be exported to the sysfs interface, and they can be overridden by pinctrl entries in the Device Tree as well as
utilities like `raspi-gpio`.

Note also that there is a delay of a few seconds between power being applied and the changes taking effect — longer
if booting over the network or from a USB mass storage device.
