# Video options in config.txt 

## Composite video mode options

### sdtv_mode

The `sdtv_mode` command defines the TV standard used for composite video output over the yellow RCA jack. The default value is `0`.

| sdtv_mode | result |
| --- | --- |
| 0 | Normal NTSC |
| 1 | Japanese version of NTSC – no pedestal |
| 2 | Normal PAL |
| 3 | Brazilian version of PAL – 525/60 rather than 625/50, different subcarrier |
| 16 | Progressive scan NTSC |
| 18 | Progressive scan PAL |

### sdtv_aspect

The `sdtv_aspect` command defines the aspect ratio for composite video output. The default value is `1`.

| sdtv_aspect | result |
| --- | --- |
| 1 | 4:3 |
| 2 | 14:9 |
| 3 | 16:9 |

### sdtv_disable_colourburst

Setting `sdtv_disable_colourburst` to `1` disables colourburst on composite video output. The picture will be displayed in monochrome, but it may appear sharper.

### enable_tvout (Pi 4B only)

On the Raspberry Pi 4, composite output is disabled by default, due to the way the internal clocks are interrelated and allocated. Because composite video requires a very specific clock, setting that clock to the required speed on the Pi 4 means that other clocks connected to it are detrimentally affected, which slightly slows down the entire system. Since composite video is a less commonly used function, we decided to disable it by default to prevent this system slowdown. 

To enable composite output, use the `enable_tvout=1` option. As described above, this will detrimentally affect performance to a small degree.

On older Pi models, the composite behaviour remains the same.

## HDMI mode options

**Note for Raspberry Pi4B users:** Because the Raspberry Pi 4B has two HDMI ports, some HDMI commands can be applied to either port. You can use the syntax `<command>:<port>`, where port is 0 or 1, to specify which port the setting should apply to. If no port is specified, the default is 0. If you specify a port number on a command that does not require a port number, the port is ignored. Further details on the syntax and alternatives mechanisms can be found on the [conditionals page](./conditional.md) in the HDMI section of the documentation. 

### hdmi_safe

Setting `hdmi_safe` to `1` will lead to "safe mode" settings being used to try to boot with maximum HDMI compatibility. This is the same as setting the following parameters:

```
hdmi_force_hotplug=1
hdmi_ignore_edid=0xa5000080
config_hdmi_boost=4
hdmi_group=2
hdmi_mode=4
disable_overscan=0
overscan_left=24
overscan_right=24
overscan_top=24
overscan_bottom=24
```

### hdmi_ignore_edid

Setting `hdmi_ignore_edid` to `0xa5000080` enables the ignoring of EDID/display data if your display does not have an accurate [EDID](https://en.wikipedia.org/wiki/Extended_display_identification_data). It requires this unusual value to ensure that it is not triggered accidentally.

### hdmi_edid_file

Setting `hdmi_edid_file` to `1` will cause the GPU to read EDID data from the `edid.dat` file, located in the boot partition, instead of reading it from the monitor. More information is available [here](https://www.raspberrypi.org/forums/viewtopic.php?p=173430#p173430).

### hdmi_edid_filename

On the Raspberry Pi 4B, you can use the `hdmi_edid_filename` command to specify the filename of the EDID file to use, and also to specify which port the file is to be applied to. This also requires `hdmi_edid_file=1` to enable EDID files.

For example:

```
hdmi_edid_file=1
hdmi_edid_filename:0=FileForPortZero.edid
hdmi_edid_filename:1=FileForPortOne.edid
```

### hdmi_force_edid_audio

Setting `hdmi_force_edid_audio` to `1` pretends that all audio formats are supported by the display, allowing passthrough of DTS/AC3 even when this is not reported as supported.

### hdmi_ignore_edid_audio

Setting `hdmi_ignore_edid_audio` to `1` pretends that all audio formats are unsupported by the display. This means ALSA will default to the analogue audio (headphone) jack.

### hdmi_force_edid_3d

Setting `hdmi_force_edid_3d` to `1` pretends that all CEA modes support 3D, even when the EDID does not indicate support for this.

### hdmi_ignore_cec_init

Setting `hdmi_ignore_cec_init` to `1` will stop the initial active source message being sent during bootup. This prevents a CEC-enabled TV from coming out of standby and channel-switching when you are rebooting your Raspberry Pi.

### hdmi_ignore_cec

Setting `hdmi_ignore_cec` to `1` pretends that [CEC](https://en.wikipedia.org/wiki/Consumer_Electronics_Control#CEC) is not supported at all by the TV. No CEC functions will be supported.

### cec_osd_name

The `cec_osd_name` command sets the initial CEC name of the device. The default is Raspberry Pi.

### hdmi_pixel_encoding

The `hdmi_pixel_encoding` command forces the pixel encoding mode. By default, it will use the mode requested from the EDID, so you shouldn't need to change it.

| hdmi_pixel_encoding | result |
| --- | --- |
| 0 | default (RGB limited for CEA, RGB full for DMT) |
| 1 | RGB limited (16-235) |
| 2 | RGB full (0-255) |
| 3 | YCbCr limited (16-235) |
| 4 | YCbCr full (0-255) |

### hdmi_blanking

The `hdmi_blanking` command allows you to choose whether the HDMI output should be switched off when DPMS is triggered. This is to mimic the behaviour of other computers. After a specific amount of time, the display will become blank and go into low-power/standby mode due to receiving no signal.

**NOTE:** This feature may cause issues when using applications which don't use the framebuffer, such as omxplayer.

| hdmi_blanking | result |
| --- | --- |
| 0 | HDMI Output will blank instead of being disabled |
| 1 | HDMI Output will be disabled rather than just blanking |

### hdmi_drive

The `hdmi_drive` command allows you to choose between HDMI and DVI output modes.

| hdmi_drive | result |
| --- | --- |
| 1 | Normal DVI mode (no sound) |
| 2 | Normal HDMI mode (sound will be sent if supported and enabled) |

### config_hdmi_boost

Configures the signal strength of the HDMI interface. The default value is `0` and the maximum is `11`.

The default value for the original Model B and A is `2`. The default value for the Model B+ and all later models is `5`.

If you are seeing HDMI issues (speckling, interference) then try `7`. Very long HDMI cables may need up to `11`, but values this high should not be used unless absolutely necessary.

### hdmi_group

The `hdmi_group` command defines the HDMI output group to be either CEA (Consumer Electronics Association, the standard typically used by TVs) or DMT (Display Monitor Timings, the standard typically used by monitors). This setting should be used in conjunction with `hdmi_mode`.

| hdmi_group | result |
| --- | --- |
| 0 | Auto-detect from EDID |
| 1 | CEA |
| 2 | DMT |

### hdmi_mode

Together with `hdmi_group`, `hdmi_mode` defines the HDMI output format.

To set a custom display mode not listed here, see [this thread](https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=24679).

These values are valid if `hdmi_group=1` (CEA):

| hdmi_mode | resolution | frequency | notes |
| --- | --- | --- | --- |
| 1 | VGA (640x480) |  |  |
| 2 | 480p | 60Hz |  |
| 3 | 480p | 60Hz | 16:9 aspect ratio |
| 4 | 720p | 60Hz |  |
| 5 | 1080i | 60Hz |  |
| 6 | 480i | 60Hz |  |
| 7 | 480i | 60Hz | 16:9 aspect ratio |
| 8 | 240p | 60Hz |  |
| 9 | 240p | 60Hz | 16:9 aspect ratio |
| 10 | 480i | 60Hz | pixel quadrupling |
| 11 | 480i | 60Hz | pixel quadrupling, 16:9 aspect ratio |
| 12 | 240p | 60Hz | pixel quadrupling |
| 13 | 240p | 60Hz | pixel quadrupling, 16:9 aspect ratio |
| 14 | 480p | 60Hz | pixel doubling |
| 15 | 480p | 60Hz | pixel doubling, 16:9 aspect ratio |
| 16 | 1080p | 60Hz |  |
| 17 | 576p | 50Hz |  |
| 18 | 576p | 50Hz | 16:9 aspect ratio |
| 19 | 720p | 50Hz |  |
| 20 | 1080i | 50Hz |  |
| 21 | 576i | 50Hz |  |
| 22 | 576i | 50Hz | 16:9 aspect ratio |
| 23 | 288p | 50Hz |  |
| 24 | 288p | 50Hz | 16:9 aspect ratio |
| 25 | 576i | 50Hz | pixel quadrupling |
| 26 | 576i | 50Hz | pixel quadrupling, 16:9 aspect ratio |
| 27 | 288p | 50Hz | pixel quadrupling |
| 28 | 288p | 50Hz | pixel quadrupling, 16:9 aspect ratio |
| 29 | 576p | 50Hz | pixel doubling |
| 30 | 576p | 50Hz | pixel doubling, 16:9 aspect ratio |
| 31 | 1080p | 50Hz |  |
| 32 | 1080p | 24Hz |  |
| 33 | 1080p | 25Hz |  |
| 34 | 1080p | 30Hz |  |
| 35 | 480p | 60Hz | pixel quadrupling |
| 36 | 480p | 60Hz | pixel quadrupling, 16:9 aspect ratio |
| 37 | 576p | 50Hz | pixel quadrupling |
| 38 | 576p | 50Hz | pixel quadrupling, 16:9 aspect ratio |
| 39 | 1080i | 50Hz | reduced blanking |
| 40 | 1080i | 100Hz |  |
| 41 | 720p | 100Hz |  |
| 42 | 576p | 100Hz |  |
| 43 | 576p | 100Hz | 16:9 aspect ratio |
| 44 | 576i | 100Hz |  |
| 45 | 576i | 100Hz | 16:9 aspect ratio |
| 46 | 1080i | 120Hz |  |
| 47 | 720p | 120Hz |  |
| 48 | 480p | 120Hz |  |
| 49 | 480p | 120Hz | 16:9 aspect ratio |
| 50 | 480i | 120Hz |  |
| 51 | 480i | 120Hz | 16:9 aspect ratio |
| 52 | 576p | 200Hz |  |
| 53 | 576p | 200Hz | 16:9 aspect ratio |
| 54 | 576i | 200Hz |  |
| 55 | 576i | 200Hz | 16:9 aspect ratio |
| 56 | 480p | 240Hz |  |
| 57 | 480p | 240Hz | 16:9 aspect ratio |
| 58 | 480i | 240Hz |  |
| 59 | 480i | 240Hz | 16:9 aspect ratio |

In the table above, the modes with a 16:9 aspect ratio are a widescreen variant of a mode which usually has 4:3 aspect ratio. Pixel doubling and quadrupling indicates a higher clock rate, with each pixel repeated two or four times respectively.

These values are valid if `hdmi_group=2` (DMT):

| hdmi_mode | resolution | frequency | notes |
| --- | --- | --- | --- |
| 1 | 640x350 | 85Hz |  |
| 2 | 640x400 | 85Hz |  |
| 3 | 720x400 | 85Hz |  |
| 4 | 640x480 | 60Hz |  |
| 5 | 640x480 | 72Hz |  |
| 6 | 640x480 | 75Hz |  |
| 7 | 640x480 | 85Hz |  |
| 8 | 800x600 | 56Hz |  |
| 9 | 800x600 | 60Hz |  |
| 10 | 800x600 | 72Hz |  |
| 11 | 800x600 | 75Hz |  |
| 12 | 800x600 | 85Hz |  |
| 13 | 800x600 | 120Hz |  |
| 14 | 848x480 | 60Hz |  |
| 15 | 1024x768 | 43Hz | incompatible with the Raspberry Pi |
| 16 | 1024x768 | 60Hz |  |
| 17 | 1024x768 | 70Hz |  |
| 18 | 1024x768 | 75Hz |  |
| 19 | 1024x768 | 85Hz |  |
| 20 | 1024x768 | 120Hz |  |
| 21 | 1152x864 | 75Hz |  |
| 22 | 1280x768 |  | reduced blanking |
| 23 | 1280x768 | 60Hz |  |
| 24 | 1280x768 | 75Hz |  |
| 25 | 1280x768 | 85Hz |  |
| 26 | 1280x768 | 120Hz | reduced blanking |
| 27 | 1280x800 |  | reduced blanking |
| 28 | 1280x800 | 60Hz |  |
| 29 | 1280x800 | 75Hz |  |
| 30 | 1280x800 | 85Hz |  |
| 31 | 1280x800 | 120Hz | reduced blanking |
| 32 | 1280x960 | 60Hz |  |
| 33 | 1280x960 | 85Hz |  |
| 34 | 1280x960 | 120Hz | reduced blanking |
| 35 | 1280x1024 | 60Hz |  |
| 36 | 1280x1024 | 75Hz |  |
| 37 | 1280x1024 | 85Hz |  |
| 38 | 1280x1024 | 120Hz | reduced blanking |
| 39 | 1360x768 | 60Hz |  |
| 40 | 1360x768 | 120Hz | reduced blanking |
| 41 | 1400x1050 |  | reduced blanking |
| 42 | 1400x1050 | 60Hz |  |
| 43 | 1400x1050 | 75Hz |  |
| 44 | 1400x1050 | 85Hz |  |
| 45 | 1400x1050 | 120Hz | reduced blanking |
| 46 | 1440x900 |  | reduced blanking |
| 47 | 1440x900 | 60Hz |  |
| 48 | 1440x900 | 75Hz |  |
| 49 | 1440x900 | 85Hz |  |
| 50 | 1440x900 | 120Hz | reduced blanking |
| 51 | 1600x1200 | 60Hz |  |
| 52 | 1600x1200 | 65Hz |  |
| 53 | 1600x1200 | 70Hz |  |
| 54 | 1600x1200 | 75Hz |  |
| 55 | 1600x1200 | 85Hz |  |
| 56 | 1600x1200 | 120Hz | reduced blanking |
| 57 | 1680x1050 |  | reduced blanking |
| 58 | 1680x1050 | 60Hz |  |
| 59 | 1680x1050 | 75Hz |  |
| 60 | 1680x1050 | 85Hz |  |
| 61 | 1680x1050 | 120Hz | reduced blanking |
| 62 | 1792x1344 | 60Hz |  |
| 63 | 1792x1344 | 75Hz |  |
| 64 | 1792x1344 | 120Hz | reduced blanking |
| 65 | 1856x1392 | 60Hz |  |
| 66 | 1856x1392 | 75Hz |  |
| 67 | 1856x1392 | 120Hz | reduced blanking |
| 68 | 1920x1200 |  | reduced blanking |
| 69 | 1920x1200 | 60Hz |  |
| 70 | 1920x1200 | 75Hz |  |
| 71 | 1920x1200 | 85Hz |  |
| 72 | 1920x1200 | 120Hz | reduced blanking |
| 73 | 1920x1440 | 60Hz |  |
| 74 | 1920x1440 | 75Hz |  |
| 75 | 1920x1440 | 120Hz | reduced blanking |
| 76 | 2560x1600 |  | reduced blanking |
| 77 | 2560x1600 | 60Hz |  |
| 78 | 2560x1600 | 75Hz |  |
| 79 | 2560x1600 | 85Hz |  |
| 80 | 2560x1600 | 120Hz | reduced blanking |
| 81 | 1366x768 | 60Hz |  |
| 82 | 1920x1080 | 60Hz | 1080p |
| 83 | 1600x900 |  | reduced blanking |
| 84 | 2048x1152 |  | reduced blanking |
| 85 | 1280x720 | 60Hz | 720p |
| 86 | 1366x768 |  | reduced blanking |

Note that there is a [pixel clock limit](https://www.raspberrypi.org/forums/viewtopic.php?f=26&t=20155&p=195443#p195443).The highest supported mode is 1920x1200 at 60Hz with reduced blanking.

### hdmi_timings

This allows setting of raw HDMI timing values for a custom mode, selected using `hdmi_group=2` and `hdmi_mode=87`.

```
hdmi_timings=<h_active_pixels> <h_sync_polarity> <h_front_porch> <h_sync_pulse> <h_back_porch> <v_active_lines> <v_sync_polarity> <v_front_porch> <v_sync_pulse> <v_back_porch> <v_sync_offset_a> <v_sync_offset_b> <pixel_rep> <frame_rate> <interlaced> <pixel_freq> <aspect_ratio>
```

```
<h_active_pixels> = horizontal pixels (width)  
<h_sync_polarity> = invert hsync polarity  
<h_front_porch>   = horizontal forward padding from DE acitve edge  
<h_sync_pulse>    = hsync pulse width in pixel clocks  
<h_back_porch>    = vertical back padding from DE active edge  
<v_active_lines>  = vertical pixels height (lines)  
<v_sync_polarity> = invert vsync polarity  
<v_front_porch>   = vertical forward padding from DE active edge  
<v_sync_pulse>    = vsync pulse width in pixel clocks  
<v_back_porch>    = vertical back padding from DE active edge  
<v_sync_offset_a> = leave at zero  
<v_sync_offset_b> = leave at zero  
<pixel_rep>       = leave at zero  
<frame_rate>      = screen refresh rate in Hz  
<interlaced>      = leave at zero  
<pixel_freq>      = clock frequency (width*height*framerate)  
<aspect_ratio>    = *  
```

`*` The aspect ratio can be set to one of eight values (choose the closest for your screen):

```
HDMI_ASPECT_4_3 = 1  
HDMI_ASPECT_14_9 = 2  
HDMI_ASPECT_16_9 = 3  
HDMI_ASPECT_5_4 = 4  
HDMI_ASPECT_16_10 = 5  
HDMI_ASPECT_15_9 = 6  
HDMI_ASPECT_21_9 = 7  
HDMI_ASPECT_64_27 = 8  
```

### hdmi_force_mode

Setting to `1` will remove all other modes except the ones specified by `hdmi_mode` and `hdmi_group` from the internal list, meaning they will not appear in any enumerated lists of modes. This option may help if a display seems to be ignoring the `hdmi_mode` and `hdmi_group` settings.

### edid_content_type

Forces the EDID content type to a specific value.

The options are:
 - `0` = `EDID_ContentType_NODATA`, content type none.
 - `1` = `EDID_ContentType_Graphics`, content type graphics, ITC must be set to 1
 - `2` = `EDID_ContentType_Photo`, content type photo
 - `3` = `EDID_ContentType_Cinema`,  content type cinema
 - `4` = `EDID_ContentType_Game`,  content type game
 
### hdmi_enable_4kp60 (Pi 4B only)

By default, when connected to a 4K monitor, the Raspberry Pi 4B will select a 30hz refresh rate. Use this option to allow selection of 60Hz refresh rates. Note, this will increase power consumption and increase the temperature of the Raspberry Pi. It is not possible to output 4Kp60 on both micro HDMI ports simultaneously.
 
## Which values are valid for my monitor?

Your HDMI monitor may only support a limited set of formats. To find out which formats are supported, use the following method:

  1. Set the output format to VGA 60Hz (`hdmi_group=1` and `hdmi_mode=1`) and boot up your Raspberry Pi
  1. Enter the following command to give a list of CEA-supported modes: `/opt/vc/bin/tvservice -m CEA`
  1. Enter the following command to give a list of DMT-supported modes: `/opt/vc/bin/tvservice -m DMT`
  1. Enter the following command to show your current state: `/opt/vc/bin/tvservice -s`
  1. Enter the following commands to dump more detailed information from your monitor: `/opt/vc/bin/tvservice -d edid.dat; /opt/vc/bin/edidparser edid.dat`

The `edid.dat` should also be provided when troubleshooting problems with the default HDMI mode.

## Custom mode

If your monitor requires a mode that is not in one of the tables above, then it's possible to define a custom [CVT](https://en.wikipedia.org/wiki/Coordinated_Video_Timings) mode for it instead:

```
hdmi_cvt=<width> <height> <framerate> <aspect> <margins> <interlace> <rb>
```

| Value | Default | Description |
| --- | --- | --- |
| width | (required) | width in pixels |
| height | (required) | height in pixels |
| framerate | (required) | framerate in Hz |
| aspect | 3 | aspect ratio 1=4:3, 2=14:9, 3=16:9, 4=5:4, 5=16:10, 6=15:9 |
| margins | 0 | 0=margins disabled, 1=margins enabled |
| interlace | 0 | 0=progressive, 1=interlaced |
| rb | 0 | 0=normal, 1=reduced blanking |

Fields at the end can be omitted to use the default values.

Note that this simply **creates** the mode (group 2 mode 87). In order to make the Pi use this by default, you must add some additional settings. For example, the following selects an 800 × 480 resolution and enables audio drive:

```
hdmi_cvt=800 480 60 6
hdmi_group=2
hdmi_mode=87
hdmi_drive=2
```

This may not work if your monitor does not support standard CVT timings.

## LCD display/touchscreen options

### ignore_lcd

By default the Raspberry Pi LCD display is used when it is detected on the I2C bus. `ignore_lcd=1` will skip this detection phase, and therefore the LCD display will not be used.

### display_default_lcd

If a Raspberry Pi DSI LCD is detected it will be used as the default display and will show the framebuffer. Setting `display_default_lcd=0` will ensure the LCD is not the default display, which usually implies the HDMI output will be the default. The LCD can still be used by choosing its display number from supported applications, for example, omxplayer.

### lcd_framerate

Specify the framerate of the Raspberry Pi LCD display, in Hertz/fps. Defaults to 60Hz.

### lcd_rotate

This flips the display using the LCD's inbuilt flip functionality, which is a cheaper operation that using the GPU-based rotate operation.

For example, `lcd_rotate=2` will compensate for an upside down display.

### disable_touchscreen

Enable/disable the touchscreen.

`disable_touchscreen=1` will disable the touchscreen on the official Raspberry Pi LCD display.

### enable_dpi_lcd

Enable LCD displays attached to the DPI GPIOs. This is to allow the use of third-party LCD displays using the parallel display interface.

### dpi_group, dpi_mode, dpi_output_format

The `dpi_group` and `dpi_mode` config.txt parameters are used to set either predetermined modes (DMT or CEA modes as used by HDMI above). A user can generate custom modes in much the same way as for HDMI (see `dpi_timings` section).

`dpi_output_format` is a bitmask specifying various parameters used to set up the display format. 

More details on using the DPI modes and the output format can be found [here](../../hardware/raspberrypi/dpi/README.md).

### dpi_timings

This allows setting of raw DPI timing values for a custom mode, selected using `dpi_group=2` and `dpi_mode=87`.

```
dpi_timings=<h_active_pixels> <h_sync_polarity> <h_front_porch> <h_sync_pulse> <h_back_porch> <v_active_lines> <v_sync_polarity> <v_front_porch> <v_sync_pulse> <v_back_porch> <v_sync_offset_a> <v_sync_offset_b> <pixel_rep> <frame_rate> <interlaced> <pixel_freq> <aspect_ratio>
```

```
<h_active_pixels> = horizontal pixels (width)  
<h_sync_polarity> = invert hsync polarity  
<h_front_porch>   = horizontal forward padding from DE acitve edge  
<h_sync_pulse>    = hsync pulse width in pixel clocks  
<h_back_porch>    = vertical back padding from DE active edge  
<v_active_lines>  = vertical pixels height (lines)  
<v_sync_polarity> = invert vsync polarity  
<v_front_porch>   = vertical forward padding from DE active edge  
<v_sync_pulse>    = vsync pulse width in pixel clocks  
<v_back_porch>    = vertical back padding from DE active edge  
<v_sync_offset_a> = leave at zero  
<v_sync_offset_b> = leave at zero  
<pixel_rep>       = leave at zero  
<frame_rate>      = screen refresh rate in Hz  
<interlaced>      = leave at zero  
<pixel_freq>      = clock frequency (width*height*framerate)  
<aspect_ratio>    = *
```

`*` The aspect ratio can be set to one of eight values (choose the closest for your screen):

```
HDMI_ASPECT_4_3 = 1  
HDMI_ASPECT_14_9 = 2  
HDMI_ASPECT_16_9 = 3  
HDMI_ASPECT_5_4 = 4  
HDMI_ASPECT_16_10 = 5  
HDMI_ASPECT_15_9 = 6  
HDMI_ASPECT_21_9 = 7  
HDMI_ASPECT_64_27 = 8  
```

## Generic display options

### hdmi_force_hotplug

Setting `hdmi_force_hotplug` to `1` pretends that the HDMI hotplug signal is asserted, so it appears that a HDMI display is attached. In other words, HDMI output mode will be used, even if no HDMI monitor is detected.

### hdmi_ignore_hotplug

Setting `hdmi_ignore_hotplug` to `1` pretends that the HDMI hotplug signal is not asserted, so it appears that a HDMI display is not attached. In other words, composite output mode will be used, even if an HDMI monitor is detected.

### disable_overscan

Set `disable_overscan` to `1` to disable the default values of [overscan](../raspi-config.md#overscan) that is set by the firmware. The default value of overscan for the left, right, top, and bottom edges is `48` for HD CEA modes, `32` for SD CEA modes, and `0` for DMT modes. The default value for `disable_overscan` is `0`.

**NOTE:** any further additional overscan options such as `overscan_scale` or overscan edges can still be applied after this option.

### overscan_left

The `overscan_left` command specifies the number of pixels to add to the firmware default value of overscan on the left edge of the screen. The default value is `0`.

Increase this value if the text flows off the left edge of the screen; decrease it if there is a black border between the left edge of the screen and the text.

### overscan_right

The `overscan_right` command specifies the number of pixels to add to the firmware default value of overscan on the right edge of the screen. The default value is `0`.

Increase this value if the text flows off the right edge of the screen; decrease it if there is a black border between the right edge of the screen and the text.

### overscan_top

The `overscan_top` command specifies the number of pixels to add to the firmware default value of overscan on the top edge of the screen. The default value is `0`.

Increase this value if the text flows off the top edge of the screen; decrease it if there is a black border between the top edge of the screen and the text.

### overscan_bottom

The `overscan_bottom` command specifies the number of pixels to add to the firmware default value of overscan on the bottom edge of the screen. The default value is `0`.

Increase this value if the text flows off the bottom edge of the screen; decrease it if there is a black border between the bottom edge of the screen and the text.

### overscan_scale

Set `overscan_scale` to `1` to force any non-framebuffer layers to conform to the overscan settings. The default value is `0`.

**NOTE:** this feature is generally not recommended: it can reduce image quality because all layers on the display will be scaled by the GPU. Disabling overscan on the display itself is the recommended option to avoid images being scaled twice (by the GPU and the display).

### framebuffer_width

The `framebuffer_width` command specifies the console framebuffer width in pixels. The default is the display width minus the total horizontal overscan.

### framebuffer_height

The `framebuffer_height` command specifies the console framebuffer height in pixels. The default is the display height minus the total vertical overscan.

### max_framebuffer_height, max_framebuffer_width

Specifies the maximum dimensions that the internal frame buffer is allowed to be. 

### framebuffer_depth

Use `framebuffer_depth` to specify the console framebuffer depth in bits per pixel. The default value is `16`.

| framebuffer_depth | result | notes |
| --- | --- | --- |
| 8 |  8bit framebuffer | Default RGB palette makes screen unreadable |
| 16 | 16bit framebuffer | |
| 24 | 24bit framebuffer | May result in a corrupted display |
| 32 | 32bit framebuffer | May need to be used in conjunction with `framebuffer_ignore_alpha=1` |

### framebuffer_ignore_alpha

Set `framebuffer_ignore_alpha` to `1` to disable the alpha channel. Can help with the display of a 32bit `framebuffer_depth`.

### test_mode

The `test_mode` command displays a test image and sound during boot (over the composite video and analogue audio outputs only) for the given number of seconds, before continuing to boot the OS as normal. This is used as a manufacturing test; the default value is `0`.

### display_hdmi_rotate

Use `display_hdmi_rotate` to rotate or flip the HDMI display orientation. The default value is `0`.

| display_hdmi_rotate | result |
| --- | --- |
| 0 | no rotation |
| 1 | rotate 90 degrees clockwise |
| 2 | rotate 180 degrees clockwise |
| 3 | rotate 270 degrees clockwise |
| 0x10000 | horizontal flip |
| 0x20000 | vertical flip |

Note that the 90 and 270 degree rotation options require additional memory on the GPU, so these will not work with the 16MB GPU split.

If using the VC4 FKMS V3D driver (this is the default on the Raspberry Pi 4), then 90 and 270 degree rotations are not supported. The Screen Configuration utility provides display rotations for this driver.

### display_lcd_rotate

Use `display_lcd_rotate` to rotate or flip the LCD orientation. Parameters are the same as `display_hdmi_rotate`.

### display_rotate

`display_rotate` is deprecated in the latest firmware but has been retained for backwards compatibility. Please use `display_lcd_rotate` and `display_hdmi_rotate` instead.

Use `display_rotate` to rotate or flip the screen orientation. Parameters are the same as `display_hdmi_rotate`.

## Other options

### dispmanx_offline

Forces dispmanx composition to be done offline in two offscreen framebuffers. This can allow more dispmanx elements to be composited, but is slower and may limit screen framerate to typically 30fps.

*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
