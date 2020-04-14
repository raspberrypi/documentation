## How to rotate your display

The options to rotate the display of your Raspberry Pi depend on which display driver software it is running, which may also depend on which Raspberry Pi you are using. 

### Fake or Full KMS graphics driver (Default on Pi4)

If you are running the Raspberry Pi desktop then rotation is achieved by using the `Screen Configuration Utility` from the desktop `Preferences` menu. This will bring up a graphical representation of the display or displays connected tothe Raspberry Pi. Right click on the display you wish to rotate and select the required option.

It is also possible to change these settings using the command line `xrandr` option.

```bash
DISPLAY=:0 xrandr --output HDMI1 --rotate left 
DISPLAY=:0 xrandr --output HDMI1 --rotate inverted
DISPLAY=:0 xrandr --output HDMI1 --rotate normal
```

If you are using the console only (no graphical desktop) then you will need to set the appropriate kernel command line flags. Change the console settings as described on the [this page](./cmdline-txt.md).

### Legacy graphics driver (default on models prior to the Pi4)

There are `config.txt` options for rotating when using the legacy display drivers. 

`display_hdmi_rotate` is used to rotate the HDMI display, `display_lcd_rotate` is used to rotate any attached LCD panel (using the DSI or DPI interface). Each option takes one of the following parameters :

| display_*_rotate | result |
| --- | --- |
| 0 | no rotation |
| 1 | rotate 90 degrees clockwise |
| 2 | rotate 180 degrees clockwise |
| 3 | rotate 270 degrees clockwise |
| 0x10000 | horizontal flip |
| 0x20000 | vertical flip |
Note that the 90 and 270 degree rotation options require additional memory on the GPU, so these will not work with the 16MB GPU split.

### Rotating a touchscreen
