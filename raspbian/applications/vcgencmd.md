## vcgencmd

`vcgencmd` is a command line utility that can get various pieces of information from the VideoCore GPU on the Raspberry Pi. Much of the information available is only of use to Raspberry Pi engineers, but there are a number of very useful options available to end users that will be described here.

The source for the application can be found on our github page [here](https://github.com/raspberrypi/userland/tree/master/host_applications/linux/apps/gencmd).


### Usage

To get a list of all the commands that `vcgencmd` supports, type `vcgencmd commands`.

Some of the more useful  commands are described below.

### Commands 

#### vcos

The `vcos` cammand has a number of sub commands

`version` Displays the build date and version of the firmware on the VideoCore.
`log status` Displays the error log status of the various VideoCore software areas.

#### version

Displays the build date and version of the firmware on the VideoCore.

#### get_camera

Displays the enabled and detected state of the official camera. 1 means yes, 0 means no. Whilst all firmware (except cutdown versions) will support the camera, this support needs to be enabled by using [raspi-config](../../configuration/raspi-config.md).

#### get_throttled

Returns the throttled state of the system. This is a bit pattern.

| Bit | Meaning |
|:---:|---------|
| 0   | Under-voltage detected |
| 1   | Arm frequency capped |
| 2   | Currently throttled |
| 3   | Soft temperature limit active |
| 16  | Under-voltage has occurred |
| 17  | Arm frequency capped has occurred |
| 18  | Throttling has occurred |
| 19  | Soft temperature limit has occurred |

For example, 0x50000 has bits 16 and 18 set, indicating that the Pi has previously been throttled due to under-voltage, but is not currently throttled for any reason.

#### measure_temp

Returns the temperature of the SoC as measured by the on-board temperature sensor

#### measure_clock [clock]

This returns the current frequency of the specified clock. The options are:

| clock | Description |
|:-----:|-------------|
| arm   | ARM cores |
| core  | VC4 scaler cores |
| H264  | H264 block |
| isp   | Image Signal Processor |
| v3d   | 3D block |
| uart  | UART |
| pwm   | PWM block (analogue audio output) | 
| emmc  | SD card interface |
| pixel | Pixel valve |
| vec | Analogue video encoder |
| hdmi | HDMI |
| dpi | Display Peripheral Interface |

e.g. `vcgencmd measure_clock arm`

#### measure_volts [block]

Displays the current voltages used by the specific block.

| block | Description |
|:-----:|-------------|
| core | VC4 core voltage |
| sdram_c | |
| sdram_i | |
| sdram_p | |

#### otp_dump

Displays the content of the One Time Programmable (OTP) memory, which is part of the SoC. These are 32 bit values, indexed from 8 to 64. See the [OTP bits page](../../../hardware/raspberrypi/otpbits.md) for more details.

#### get_mem

Reports on the amount of memory allocated to the ARM cores `vcgencmd get_mem arm` and the VC4 `vcgencmd get_mem gpu`.

**Note:** On a Raspberry Pi 4 with greater than 1GB of RAM, the `arm` option is inaccurate. This is because the GPU firmware which implements this command is only aware of the first gigabyte of RAM on the system, so the `arm` setting will always return 1GB minus the `gpu` memory value. To get an accurate report of the amount of ARM memory, use one of the standard Linux commands, such as `free` or `cat /proc/meminfo`

#### codec_enabled [type]

Reports whether the specified CODEC type is enabled. Possible options for type are AGIF, FLAC, H263, H264, MJPA, MJPB, MJPG, **MPG2**, MPG4, MVC0, PCM, THRA, VORB, VP6, VP8, **WMV9**, **WVC1**. Those highlighted currently require a paid for licence, except on the Pi4, where these hardware codecs are disabled in preference to software decoding, which requires no licence.

#### get_config type | name

This returns all the configuration items of the specified type that have been set in config.txt, or a single configuration item. Possible values for type parameter are **int, str**, or simply use the name of the configuration item.

#### get_lcd_info

Displays the resolution and colour depth of any attached display.

#### mem_oom

Displays statistics on any Out Of Memory events occuring in the VC4 memory space.

#### mem_reloc_stats

Displays statistics from the relocatable memory allocator on the VC4.

#### read_ring_osc

Returns the curent speed voltage and temperature of the ring oscillator.

#### hdmi_timings

Displays the current HDMI settings timings. See [Video Config](../../configuration/config-txt/video.md) for details of the values returned. 

#### dispmanx_list

Dump a list of all dispmanx items currently being displayed.

#### display_power

Show current display power state, or set the display power state. `vcgencmd display_power 0` will turn off power to the current display. `vcgencmd display_power 1` will turn on power to the display. If no parameter is set, this will display the current power state. The final parameter is an optional display ID, as returned by `tvservice -l`, which allows a specific display to be turned on or off.

`vcgencmd display_power 0 7` will turn off power to display ID 7, which is HDMI 1 on a Raspberry Pi 4.





