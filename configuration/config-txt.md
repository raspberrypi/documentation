# config.txt

As it's an embedded platform, the Raspberry Pi doesn't have a [BIOS](https://en.wikipedia.org/wiki/BIOS) like you'd find on a conventional PC. The various system configuration parameters that would traditionally be edited and stored using a BIOS are stored in an optional text file named `config.txt`. This is read by the GPU before the ARM (and Linux) is initialised, so it must be located on the first (boot) partition of your SD card (alongside `bootcode.bin` and `start.elf`). This file is normally accessible as `/boot/config.txt` from Linux (needs to be edited as [root](../linux/usage/root.md)); but from Windows (or OS X) it is seen as a file in the only accessible part of the card. If you need to apply some of the config settings below but you don't have a `config.txt` on your boot partition yet, then simply create it as a new text file.

Any changes will only take effect after you've rebooted your Raspberry Pi. After Linux has booted you can get the current active settings with the following commands:

`vcgencmd get_config <config>` - displays a specific config value, e.g. `vcgencmd get_config arm_freq`.

`vcgencmd get_config int` - lists all the integer config options that are set (non-zero).

`vcgencmd get_config str` - lists all the string config options that are set (non-null).

(Be aware that there's a small number of config settings that can't be retrieved using `vcgencmd` though.)

# File format

As `config.txt` is read by the early-stage boot firmware it has a very simple file format. The format is a single `property=value` statement on each line, where value is either an integer (i.e. a number) or a string. Comments may be added (or existing config values may be 'commented out', which disables them) by starting a line with the `#` character.

Here is an example file:
```
# Force the monitor to HDMI mode so that sound will be sent over HDMI cable
hdmi_drive=2
# Set monitor mode to DMT
hdmi_group=2
# Set monitor resolution to 1024x768 XGA 60Hz (HDMI_DMT_XGA_60)
hdmi_mode=16
# Make display smaller to stop text spilling off the screen
overscan_left=20
overscan_right=12
overscan_top=10
overscan_bottom=10
```

# Memory

##### gpu_mem
GPU memory in megabytes. Sets the memory split between the ARM (CPU) and GPU. ARM gets the remaining memory. Min 16. Default 64.

##### gpu_mem_256
GPU memory in megabytes for the 256MB Raspberry Pi. Ignored by the 512MB Pi. Overrides gpu_mem. Max 192. Default not set.

##### gpu_mem_512
GPU memory in megabytes for the 512MB Raspberry Pi. Ignored by the 256MB Pi. Overrides gpu_mem. Max 448. Default not set.

##### disable_l2cache
Disables ARM access to GPU's L2 cache. Needs corresponding L2 disabled kernel. Default 0.

##### disable_pvt
Disable adjusting the refresh rate of RAM every 500ms (measuring RAM temparature).

## CMA - Dynamic Memory Split

The firmware and kernel as of 19. November 2012 supports CMA (Contiguous Memory Allocator), which means the memory split between ARM and GPU is managed dynamically at runtime. However this is not [officially supported](https://github.com/raspberrypi/linux/issues/503).


You can find an [example config.txt here](http://www.raspberrypi.org/phpBB3/viewtopic.php?p=223549#p223549).

##### cma_lwm
When GPU has less than `cma_lwm` (low water mark) megabytes of memory available it will request some from ARM.

##### cma_hwm
When GPU has more than `cma_hwm` (high water mark) megabytes of memory available it will release some to ARM.

The following options need to be in `cmdline.txt` for CMA to work: `coherent_pool=6M smsc95xx.turbo_mode=N`


# Camera

##### disable_camera_led
Setting this to 1 prevents the red camera led from turning on when recording video or taking a still picture. Useful for preventing reflections when the camera is facing a window.

# Video

## Composite video mode options
##### sdtv_mode
Defines the TV standard used for composite video output over the yellow RCA jack (default=0).

| sdtv_mode | result |
| --- | --- |
| 0 | Normal NTSC |
| 1 | Japanese version of NTSC – no pedestal |
| 2 | Normal PAL |
| 3 | Brazilian version of PAL – 525/60 rather than 625/50, different subcarrier |

##### sdtv_aspect
Defines the aspect ratio for composite video output (default=1).

| sdtv_mode | result |
| --- | --- |
| 1 | 4:3 |
| 2 | 14:9 |
| 3 | 16:9 |

##### sdtv_disable_colourburst
Setting this to 1 disables colour burst on composite video output. The picture will be displayed in monochrome, but it may possibly be sharper.

## HDMI mode options
##### hdmi_safe
Setting this to 1 uses "safe mode" settings to try to boot with maximum HDMI compatibility. This is the same as the combination of:
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

##### hdmi_ignore_edid
Setting this to 0xa5000080 enables the ignoring of EDID/display data if your display doesn't have an accurate [EDID](http://en.wikipedia.org/wiki/Extended_display_identification_data). It requires this unusual value to ensure that it doesn't get triggered accidentally.

##### hdmi_edid_file
Setting this to 1, will cause the GPU to read EDID data from the `edid.dat` file (located in the boot partition) instead of from the monitor. More information [here](http://www.raspberrypi.org/phpBB3/viewtopic.php?p=173430#p173430).

##### hdmi_force_edid_audio
Setting this to 1 pretends all audio formats are supported by display, allowing passthrough of DTS/AC3 even when not reported as supported.

##### hdmi_ignore_edid_audio
Setting this to 1 pretends all audio formats are unsupported by display. This means ALSA will default to the analogue audio (headphone) jack.

##### hdmi_force_edid_3d
Setting this to 1 pretends all CEA modes support 3D, even when EDID doesn't indicate support for them.

##### avoid_edid_fuzzy_match
Setting this to 1 avoids "fuzzy matching" of modes described in EDID. Instead it will pick the standard mode with the matching resolution and closest framerate even if blanking is wrong.

##### hdmi_ignore_cec_init
Setting this to 1 will prevent the initial active source message being sent during bootup. Avoids bringing a (CEC enabled) TV out of standby and channel switching when rebooting your Raspberry Pi.

##### hdmi_ignore_cec
Setting this to 1 pretends [CEC](https://en.wikipedia.org/wiki/Consumer_Electronics_Control#CEC) is not supported at all by TV. No CEC functions will be supported.

##### hdmi_pixel_encoding
Force the pixel encoding mode. By default it will use the mode requested from EDID so shouldn't need changing.

| hdmi_pixel_encoding | result |
| --- | --- |
| 0 | RGB limited (16-235) |
| 1 | RGB full (0-255) |
| 2 | YCbCr limited (16-235) |
| 3 | YCbCr full (0-255) |

##### hdmi_drive
This allows you to choose between HDMI and DVI output modes.

| hdmi_drive | result |
| --- | --- |
| 1 | Normal DVI mode (No sound) |
| 2 | Normal HDMI mode (Sound will be sent if supported and enabled) |

##### config_hdmi_boost
Configures the signal strength of the HDMI interface. Default is 0. Try 4 if you have interference issues with HDMI. 7 is the maximum.

##### hdmi_group
This defines the HDMI output group to be either [CEA](http://en.wikipedia.org/wiki/Consumer_Electronics_Association) (Consumer Electronics Association - the standard typically used by TVs) or DMT (Display Monitor Timings - the standard typically used by monitors). This setting should be used in conjunction with `hdmi_mode`.

| hdmi_group | result |
| --- | --- |
| 0 | Auto-detect from EDID |
| 1 | CEA |
| 2 | DMT |

##### hdmi_mode
This (together with `hdmi_group`) defines the HDMI output format.

(For other modes not listed here have a look at [this thread](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=24679).)

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
| 54 | 576o | 200Hz |  |
| 55 | 576o | 200Hz | 16:9 aspect ratio |
| 56 | 480p | 240Hz |  |
| 57 | 480p | 240Hz | 16:9 aspect ratio |
| 58 | 480i | 240Hz |  |
| 59 | 480i | 240Hz | 16:9 aspect ratio |

In the table above the 16:9 aspect ratios are a variant of a mode which usually has 4:3 aspect ratio. Pixel doubling and quadrupling indicates a higher clock rate, with each pixel repeated two or four times respectively.

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

Note that there is a [pixel clock limit](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=26&t=20155&p=195443#p195443) which means the highest supported mode is 1920x1200 at 60Hz with reduced blanking.

## Which values are valid for my monitor?
Your HDMI monitor may support only a limited set of formats. To find out which formats are supported, use the following method:

  * Set the output format to VGA 60Hz (`hdmi_group=1` and `hdmi_mode=1`) and boot up your Raspberry Pi.
  * Enter the following command to give a list of CEA supported modes: `/opt/vc/bin/tvservice -m CEA`
  * Enter the following command to give a list of DMT supported modes: `/opt/vc/bin/tvservice -m DMT`
  * Enter the following command to show your current state: `/opt/vc/bin/tvservice -s`
  * Enter the following commands to dump more detailed information from your monitor: `/opt/vc/bin/tvservice -d edid.dat; /opt/vc/bin/edidparser edid.dat`

The `edid.dat` should also be provided when troubleshooting problems with the default HDMI mode.

## Generic display options

##### hdmi_force_hotplug
Setting this to 1 pretends HDMI hotplug signal is asserted so it appears a HDMI display is attached, i.e. HDMI output mode will be used even if no HDMI monitor is detected.

##### hdmi_ignore_hotplug
Setting this to 1 pretends HDMI hotplug signal is not asserted so it appears a HDMI display is not attached, i.e. composite output mode will be used even if a HDMI monitor is detected.

##### disable_overscan
Set to 1 to disable [overscan](raspi-config.md#overscan).

##### overscan_left
Number of pixels to skip on left edge of the screen. Increase this value if the text flows off the left edge of the screen, or decrease it if there's a black border between the left edge of the screen and the text.

##### overscan_right
Number of pixels to skip on right edge of screen.

##### overscan_top
Number of pixels to skip on top edge of screen.

##### overscan_bottom
Number of pixels to skip on bottom edge of screen.

##### framebuffer_width
Console framebuffer width in pixels. Default is display width minus overscan.

##### framebuffer_height
Console framebuffer height in pixels. Default is display height minus overscan.

##### framebuffer_depth
Console framebuffer depth in bits per pixel. Default is 16.

| framebuffer_depth | result | notes |
| --- | --- | --- |
| 8 |  8bit framebuffer | Default RGB palette makes screen unreadable. |
| 16 | 16bit framebuffer | |
| 24 | 24bit framebuffer | May result in a corrupted display. |
| 32 | 32bit framebuffer | May need to be used in confunction with `framebuffer_ignore_alpha=1`. |

##### framebuffer_ignore_alpha
Set to 1 to disable alpha channel. Can help with the display of a 32bit `framebuffer_depth`.

##### test_mode
Set to 1 to enable test sound/image during boot (used as a manufacturing test).

##### display_rotate
Can be ued to rotate of slip the screen orientation. Default is 0.

| display_rotate | result |
| --- | --- |
| 0 | no rotation |
| 1 | rotate 90 degrees clockwise |
| 2 | rotate 180 degrees clockwise |
| 3 | rotate 270 degrees clockwise |
| 0x10000 | horizontal flip |
| 0x20000 | vertical flip |

Note: the 90 and 270 degree rotation options require additional memory on GPU, so won't work with the 16MB GPU split.

# Licensed codecs
Hardware decoding of additional codecs can be enabled by [purchasing a licence](http://swag.raspberrypi.org/collections/software) that is locked to the CPU serial number of your Raspberry Pi.

##### decode_MPG2
Licence key to allow hardware MPEG-2 decoding, e.g. `decode_MPG2=0x12345678`

##### decode_WVC1
Licence key to allow hardware VC-1 decoding, e.g. `decode_WVC1=0x12345678`

If you've got multiple Raspberry Pis, and you've bought a codec licence for each of them, you can list multiple (up to 8) licence keys in a single `config.txt`, which enables you to swap the same SD card between the different Pis, e.g. `decode_MPG2=0x12345678,0xabcdabcd,0x87654321`

# Boot
##### disable_commandline_tags
Set to 1 to stop `start.elf` from filling in ATAGS (memory from 0x100) before launching kernel.

##### cmdline
Command line parameter string. Can be used instead of `cmdline.txt` file.

##### kernel
Alternative filename (on the boot partition) to use when loading kernel. Default is `kernel.img`.

##### kernel_address
Memory address to load the kernel image at.

##### kernel_old
Set to 1 to load the kernel at memory address 0x0.

##### ramfsfile
Optional filename (on the boot partition) of a ramfs to load. More information [here](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=63&t=10532).

##### ramfsaddr
Memory address to load the `ramfsfile` at.

##### initramfs
This specifies both the ramfs filename *and* the memory adress to load it at (it's like `ramfsfile` and `ramfsaddr` in one option), e.g. `initramfs initramf.gz 0x00800000`. **NOTE:** this option uses different syntax than all other options; you should not use `=` character here.

##### device_tree
Specifies a [device tree](http://www.raspberrypi.org/forum/viewtopic.php?f=71&t=53232) filename. This is not officially supported.

##### device_tree_address
Memory address to load the `device_tree` at.

##### init_uart_baud
Initial uart baud rate. Default 115200.

##### init_uart_clock
Initial uart clock frequency. Default 3000000 (3Mhz).

##### init_emmc_clock
Initial emmc clock frequency. Default 100000000 (100MHz).

##### boot_delay
Wait for given number of seconds in `start.elf` before loading kernel. Default 1. The total delay in milliseconds is calculated as `(1000 * boot_delay) + boot_delay_ms`. Can be useful if your SD card needs a while to 'get ready' before Linux is able to boot from it.

##### boot_delay_ms
Wait for given number of milliseconds in `start.elf` (in combination with `boot_delay`) before loading kernel. Default 0.

##### avoid_safe_mode
If set to 1, [safe_mode](http://elinux.org/RPI_safe_mode) boot won't be enabled. Default 0.

##### disable_splash
If set to 1, don't show the rainbow splash screen on boot.

# Overclocking
**NOTE:** Setting any overclocking parameters to values other than those used by [raspi-config](raspi-config.md#overclock) will set a permanent bit within the SOC, making it possible to detect that your Pi has been overclocked. This was originally set to detect a void warranty if the device had been overclocked. Since September 19th 2012 you can overclock your Pi without affecting your warranty [see here](http://www.raspberrypi.org/archives/2008).

The latest kernel has a [cpufreq](http://www.pantz.org/software/cpufreq/usingcpufreqonlinux.html) kernel driver with the "ondemand" governor enabled by default. It has no effect if you have no overclock settings.
But when you do, the ARM frequency will vary with processor load. Non-default values are only used when needed according to the governor. You can adjust the minimum values with the `*_min` config options or disable dynamic clocking with `force_turbo=1` [see here](http://www.raspberrypi.org/phpBB3/viewtopic.php?p=169726#p169726).

Overclock and overvoltage will be disabled at runtime when the SoC reaches 85°C to cool it down. You should not hit the limit, even with maximum settings at 25°C ambient temperature [see here](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=11579#p169872).

## Overclocking options

| Option | Description |
| --- | --- |
| arm_freq | Frequency of ARM in MHz. Default 700. |
| gpu_freq | Sets core_freq, h264_freq, isp_freq, v3d_freq together. Default 250. |
| core_freq | Frequency of GPU processor core in MHz. It has an impact on ARM performance since it drives L2 cache. Default 250. |
| h264_freq | Frequency of hardware video block in MHz. Default 250. |
| isp_freq | Frequency of image sensor pipeline block in MHz. Default 250. |
| v3d_freq | Frequency of 3D block in MHz. Default 250. |
| avoid_pwm_pll | Don't dedicate a pll to PWM audio. This will reduce analogue audio quality slightly. The spare PLL allows the core_freq to be set independently from the rest of the gpu allowing more control over overclocking. Default 0.|
| sdram_freq | Frequency of SDRAM in MHz. Default 400. |
| over_voltage | ARM/GPU core voltage adjust. [-16,8] equates to [0.8V,1.4V] with 0.025V steps (i.e. specifying -16 will give 0.8V as the GPU/core voltage, and specifying 8 will give 1.4V) Default is 0 (1.2V). Values above 6 are only allowed when force_turbo or current_limit_override are specified (which sets the warranty bit).|
| over_voltage_sdram | Sets over_voltage_sdram_c, over_voltage_sdram_i, over_voltage_sdram_p together. |
| over_voltage_sdram_c | SDRAM controller voltage adjust. [-16,8] equates to [0.8V,1.4V] with 0.025V steps. Default 0 (1.2V). |
| over_voltage_sdram_i | SDRAM I/O voltage adjust. [-16,8] equates to [0.8V,1.4V] with 0.025V steps. Default 0 (1.2V). |
| over_voltage_sdram_p | SDRAM phy voltage adjust. [-16,8] equates to [0.8V,1.4V] with 0.025V steps. Default 0 (1.2V). |
| force_turbo | Disables dynamic cpufreq driver and minimum settings below. Enables h264/v3d/isp overclock options. Default 0. May set warranty bit. |
| initial_turbo | Enables turbo mode from boot for the given value in seconds (up to 60) or until cpufreq sets a frequency [see here](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=6201&start=425#p180099). Can help with SD card corruption if overclocked. Default 0. |
| arm_freq_min | Minimum value of arm_freq used for dynamic clocking. Default 700. |
| core_freq_min | Minimum value of core_freq used for dynamic clocking. Default 250. |
| sdram_freq_min | Minimum value of sdram_freq used for dynamic clocking. Default 400. |
| over_voltage_min | Minimum value of over_voltage used for dynamic clocking. Default 0. |
| temp_limit | Overheat protection. Sets clocks and voltages to default when the SoC reaches this Celsius value. Setting this higher than default voids your warranty. Default 85. |
| current_limit_override | Disables SMPS current limit protection when set to "0x5A000020"; it requires this unusual value to ensure that it doesn't get triggered accidentally. Can help if you are currently hitting a reboot failure when overclocking too high [see here](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=6201&start=325#p170793). May set warranty bit. |

##### force_turbo
`force_turbo=0`

Enables dynamic clocks and voltage for the ARM core, GPU core and SDRAM.
When busy, ARM frequency goes up to `arm_freq` and down to `arm_freq_min` on idle.
`core_freq`/`core_freq_min`, `sdram_freq`/`sdram_freq_min` and `over_voltage`/`over_voltage_min` behave the same. `over_voltage` is limited to 6 (1.35V).
Non-default values for the h264/v3d/isp frequencies are ignored.

`force_turbo=1`

Disables dynamic clocking, so all frequencies and voltages stay high.
Overclocking of h264/v3d/isp GPU parts is allowed as well as setting `over_voltage` up to 8 (1.4V) [see here](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=6201&sid=852d546291ae711ffcd8bf23d3214581&start=325#p170793).

## Clocks relationship

The GPU core, h264, v3d and ISP share a [PLL](http://en.wikipedia.org/wiki/Phase-locked_loop#Clock_generation) and therefore need to have related frequencies. The ARM, SDRAM and GPU each have their own PLLs and can have unrelated frequencies [see here](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=6201&start=275#p168042).

They are calculated as:
```
  pll_freq = floor(2400 / (2 * core_freq)) * (2 * core_freq)
  gpu_freq = pll_freq / [even number]
```

The effective `gpu_freq` is automatically rounded to the nearest even integer, so asking for `core_freq=500` and `gpu_freq=300` will result in divisor of 2000/300 = 6.666 => 6 and so result in a `gpu_freq` of 333.33MHz.

##### avoid_pwm_pll
Setting this to 1 will decouple a PLL from the PWM hardware. This will in result in more noise (hiss) on the analogue audio output, but allow you to set the `gpu_freq` independently of the `core_freq`.

## Monitoring Temperature and Voltage

To view the Pi's temperature, type: `cat /sys/class/thermal/thermal_zone0/temp` (divide the result by 1000 to get the value in Celsius).

To view the Pi's current frequency, type: `cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq` (divide the result by 1000 to get the value in MHz).

To monitor the Pi's PSU voltage, you'll need a multimeter to measure between the TP1 and TP2 power supply test points, more information [here](../troubleshooting/power.md).

It's generally a good idea to keep the core temperature below 70 degrees, and the voltage above 4.8V. (Note that some, not necessarily cheap, USB power supplies fall as low as 4.2V; this is because they are usually designed to charge a 3.7V LiPo battery, rather than to supply a solid 5V to a computer). If your overclocked Raspberry Pi is getting hot, a heatsink can be helpful, especially if the Pi is to be run inside a case. A suitable heatsink is the self-adhesive BGA (ball-grid-array) 14x14x10 mm heatsink, part 674-4756 from RS Components.

## Overclocking problems

Most overclocking issues show up right away with a failure to boot. If this occurs, then you can hold down the `shift` key during the next boot, which will temporarily disable all overclocking, allowing you to boot succesfully and then edit your settings.

---

*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
