## How to rotate your display

The options to rotate the display of your Raspberry Pi depend on which display driver software it is running, which may also depend on which Raspberry Pi you are using. 

### Fake or Full KMS graphics driver (Default on Pi4)

If you are running the Raspberry Pi desktop then rotation is achieved by using the `Screen Configuration Utility` from the desktop `Preferences` menu. This will bring up a graphical representation of the display or displays connected to the Raspberry Pi. Right click on the display you wish to rotate and select the required option.

It is also possible to change these settings using the command line `xrandr` option. The following commands give 0°, -90°, +90° and 180° rotations respectively. 

```bash
xrandr --output HDMI-1 --rotate normal
xrandr --output HDMI-1 --rotate left 
xrandr --output HDMI-1 --rotate right
xrandr --output HDMI-1 --rotate inverted
```

Note that the `--output` entry specifies to which device the rotation applies. You can determine the device name by simply typing `xrandr` on the command line which will display information, including the name, for all attached devices.

You can also use the command line to mirror the display using the `--reflect` option. Reflection can be one of 'normal' 'x', 'y' or 'xy'. This causes the output contents to be reflected across the specified axes. E.g.

```bash
xrandr --output HDMI-1 --reflect x
```

If you are using the console only (no graphical desktop) then you will need to set the appropriate kernel command line flags. Change the console settings as described on the [this page](./cmdline-txt.md).

### Legacy graphics driver (default on models prior to the Pi4)

There are `config.txt` options for rotating when using the legacy display drivers. 

`display_hdmi_rotate` is used to rotate the HDMI display, `display_lcd_rotate` is used to rotate any attached LCD panel (using the DSI or DPI interface). These options rotate both the desktop and console. Each option takes one of the following parameters :

| display_*_rotate | result |
| --- | --- |
| 0 | no rotation |
| 1 | rotate 90 degrees clockwise |
| 2 | rotate 180 degrees clockwise |
| 3 | rotate 270 degrees clockwise |
| 0x10000 | horizontal flip |
| 0x20000 | vertical flip |

Note that the 90 and 270 degree rotation options require additional memory on the GPU, so these will not work with the 16MB GPU split.

You can combine the rotation settings with the flips by adding them together. You can also have both horizontal and vertical flips in the same way. E.g. A 180 degree rotation with a vertical and horizontal flip will be 0x20000 + 0x10000 + 2 = 0x30002.
