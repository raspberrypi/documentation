## VCGENCMD

`vcgencmd` is a command line utility that can get various pieces of information from the Videocore4 GPU on the Raspberry Pi. Much of the information available is only of use to internal Raspberry Pi developers, but there are number of very useful options available to end users that will be described here.

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

Displays the supported and deected state of the official camera. 1 means yes, 0 means no.

#### get_throttled

Returns the throttled state of the system. This is a bit pattern.

| Bit | Meaning |
|:---:|---------|
| 0   | under-voltage |
| 1   | arm frequency capped |
| 2   | currently throttled |
| 16  | under-voltage has occurred |
| 17  | arm frequency capped has occurred |
| 18  | throttling has occurred |
| 19  | Soft Temp limit has occurred |

#### measure_temp

Returns the temperature of the SoC as measured by the on board temperature sensor

#### measure_clock [clock]

This returns the current frequency of the specified clock. The options are:

| clock | Description |
|:-----:|-------------|
| arm   | ARM cores |
| core  | VC4 scaler cores |
| H264  | H264 block |
| isp   | Image system Pipeline |
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

#### codec_enabled [type]

Reports whether the specified CODEC type is enabled. Possible options for type are **H264, MPG2, WVC1, MPG4, MJPG, WMV9**.

#### get_config [type]

This returns all the configuration items of the specified type that have been set in config.txt or by default. Possible values for type are **int, str**

#### get_lcd_info

Displays the resolution and colour depth of any attached LCD display.

#### mem_oom

Displays statistics on any Out Of Memory events occuring in the VC4 memory space.

#### mem_reloc_stats

Displays statistics from the relocatable memory allocator on the VC4.

#### read_ring_osc

Returns the curent speed voltage and temperature of the ring oscillator.

#### hdmi_timings

Displays the current HDMI settings timings. See [Video Config](https://www.raspberrypi.org/documentation/configuration/config-txt/video.md) for details of the values returned. 

#### dispmanx_list

Dump a list of all dispmanx items currently being displayed.

#### display_power

Show or set the power the display. `vcgencmd display_power 0` will turn off power to the display. `vcgencmd display_power 1` will turn on power to the display. If no parameter is set, this will display the current power state.


