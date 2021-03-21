# vcgencmd

The `vcgencmd` tool is used to output information from the VideoCore GPU on the Raspberry Pi.

You can find source code for the `vcgencmd` utility [here](https://github.com/raspberrypi/userland/tree/master/host_applications/linux/apps/gencmd).

## commands

To get a list of all commands which `vcgencmd` supports, use `vcgencmd commands`. Some useful commands and their required parameters are listed below.

### vcos

The `vcos` command has two useful sub-commands:

- `version` displays the build date and version of the firmware on the VideoCore
- `log status` displays the error log status of the various VideoCore firmware areas

### version

Displays the build date and version of the VideoCore firmware.

### get_camera

Displays the enabled and detected state of the Raspberry Pi camera: `1` means yes, `0` means no. Whilst all firmware except cutdown versions support the camera, this support needs to be enabled by using [raspi-config](../../configuration/raspi-config.md).

### get_throttled

Returns the throttled state of the system. This is a bit pattern - a bit being set indicates the following meanings:

| Bit | Hex value | Meaning |
|:---:|-----------|---------|
| 0   | 0x1 | Under-voltage detected |
| 1   | 0x2 | Arm frequency capped |
| 2   | 0x4 | Currently throttled |
| 3   | 0x8 | Soft temperature limit active |
| 16  | 0x10000 | Under-voltage has occurred |
| 17  | 0x20000 | Arm frequency capping has occurred |
| 18  | 0x40000 | Throttling has occurred |
| 19  | 0x80000 | Soft temperature limit has occurred |

### measure_temp

Returns the temperature of the SoC as measured by the on-board temperature sensor.

### measure_clock [clock]

This returns the current frequency of the specified clock. The options are:

| clock | Description |
|:-----:|-------------|
| arm   | ARM core(s) |
| core  | GPU core |
| H264  | H.264 block |
| isp   | Image Sensor Pipeline |
| v3d   | 3D block |
| uart  | UART |
| pwm   | PWM block (analogue audio output) | 
| emmc  | SD card interface |
| pixel | Pixel valves |
| vec | Analogue video encoder |
| hdmi | HDMI |
| dpi | Display Parallel Interface |

e.g. `vcgencmd measure_clock arm`

### measure_volts [block]

Displays the current voltages used by the specific block.

| block | Description |
|:-----:|-------------|
| core | VC4 core voltage |
| sdram_c | SDRAM Core Voltage |
| sdram_i | SDRAM I/O voltage |
| sdram_p | SDRAM Phy Voltage|

### otp_dump

Displays the content of the OTP (one-time programmable) memory inside the SoC. These are 32 bit values, indexed from 8 to 64. See the [OTP bits page](../../hardware/raspberrypi/otpbits.md) for more details.

### <a name="getconfig"></a>get_config [configuration item|int|str]

Display value of the configuration setting specified: alternatively, specify either `int` (integer) or `str` (string) to see all configuration items of the given type. For example:

```
vcgencmd get_config total_mem
```

returns the total memory on the device in megabytes.

### get_mem type

Reports on the amount of memory addressable by the ARM  and the GPU. To show the amount of ARM-addressable memory use `vcgencmd get_mem arm`; to show the amount of GPU-addressable memory use `vcgencmd get_mem gpu`. Note that on devices with more than 1GB of memory the `arm` parameter will always return 1GB minus the `gpu` memory value, since the GPU firmware is only aware of the first 1GB of memory. To get an accurate report of the total memory on the device, see the `total_mem` configuration item - see [`get_config`](#getconfig) section above.

#### codec_enabled [type]

Reports whether the specified CODEC type is enabled. Possible options for type are AGIF, FLAC, H263, H264, MJPA, MJPB, MJPG, **MPG2**, MPG4, MVC0, PCM, THRA, VORB, VP6, VP8, **WMV9**, **WVC1**. Those highlighted currently require a paid for licence (see the [FAQ](../../faqs/README.md#pi-video) for more info), except on the Pi 4 and 400, where these hardware codecs are disabled in preference to software decoding, which requires no licence. Note that because the H.265 HW block on the Raspberry Pi 4 and 400 is not part of the VideoCore GPU, its status is not accessed via this command.

#### get_lcd_info

Displays the resolution and colour depth of any attached display.

#### mem_oom

Displays statistics on any OOM (out of memory) events occuring in the VideoCore memory space.

#### mem_reloc_stats

Displays statistics from the relocatable memory allocator on the VideoCore.

#### read_ring_osc

Returns the curent speed voltage and temperature of the ring oscillator.

#### hdmi_timings

Displays the current HDMI settings timings. See [Video Config](../../configuration/config-txt/video.md) for details of the values returned. 

#### dispmanx_list

Dump a list of all dispmanx items currently being displayed.

#### display_power [0 | 1 | -1] [display]

Show current display power state, or set the display power state. `vcgencmd display_power 0` will turn off power to the current display. `vcgencmd display_power 1` will turn on power to the display. If no parameter is set, this will display the current power state. The final parameter is an optional display ID, as returned by `tvservice -l` or from the table below, which allows a specific display to be turned on or off.

Note that for the 7" Raspberry Pi Touch Display this simply turns the backlight on and off. The touch functionality continues to operate as normal.

`vcgencmd display_power 0 7` will turn off power to display ID 7, which is HDMI 1 on a Raspberry Pi 4.

| Display | ID |
| --- | --- | 
|Main LCD       | 0 |
|Secondary LCD  | 1 | 
|HDMI 0         | 2 |
|Composite      | 3 | 
|HDMI 1         | 7 |

To determine if a specific display ID is on or off, use -1 as the first parameter.

`vcgencmd display_power -1 7` will return 0 if display ID 7 is off, 1 if display ID 7 is on, or -1 if display ID 7 is in an unknown state, for example undetected. 
