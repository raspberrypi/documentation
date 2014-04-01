# config.txt

As the raspberry PI doesn't have a conventional BIOS, the various system configuration parameters that would normally be kept and set using a BIOS are stored as a text file named "config.txt".

The Raspberry Pi config.txt file is read by the GPU before the ARM core is initialised. 

This file is an optional file on the boot partition.  It is normally accessible as /boot/config.txt from Linux, but from Windows (or OS X) it is seen as a file in the accessible part of the card.

You can get your current active settings with the following commands:
```
 vcgencmd get_config <config> - lists a specific config value. E.g. vcgencmd get_config arm_freq
 vcgencmd get_config int - lists all the integer config options that are set (non-zero)
 vcgencmd get_config str - lists all the string config options that are set (non-null)
```

# File format

The format is "property=value" where value is an integer. You may specify only one option per line. Comments may be added by starting a line with the '#' character.                                                                                                                                     

Note: In the newer Raspberry Pi models there is # before every line. If you want changes to have an effect then 'uncomment', (i.e. remove the #).

Here is an example file:
```
 # Set stdv mode to PAL (as used in Europe)
 sdtv_mode=2
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

```disable_l2cache```	 disables ARM access to GPU's L2 cache. Needs corresponding L2 disabled kernel. Default 0.

```gpu_mem```	 GPU memory in megabyte. Sets the memory split between the ARM and GPU. ARM gets the remaining memory. Min 16. Default 64.

```gpu_mem_256```	GPU memory in megabyte for the 256MB Raspberry Pi. Ignored by the 512MB RP. Overrides gpu_mem. Max 192. Default not set.

```gpu_mem_512```	GPU memory in megabyte for the 512MB Raspberry Pi. Ignored by the 256MB RP. Overrides gpu_mem. Max 448. Default not set.

```disable_pvt```       Disable adjusting the refresh rate of RAM every 500ms (measuring RAM temparature).

## CMA - Dynamic Memory Split

The firmware and kernel as of 19. November 2012 supports CMA, which means the memory split between ARM and GPU is managed dynamically at runtime. 

You can find an [example config.txt here](http://www.raspberrypi.org/phpBB3/viewtopic.php?p=223549#p223549).

```cma_lwm```	When GPU has less than cma_lwm (low water mark) memory available it will request some from ARM.

```cma_hwm```	When GPU has more than cma_hwm (high water mark) memory available it will release some to ARM.

The following options need to be in cmdline.txt for CMA to work:
  coherent_pool=6M smsc95xx.turbo_mode=N

Note: As per https://github.com/raspberrypi/linux/issues/503 popcornmix states that CMA is not officially supported.

# Camera

```disable_camera_led``` turns off the red camera led when recording video or taking a still picture.
  disable_camera_led=1

# Video
## Video mode options
```sdtv_mode``` defines the TV standard for composite output (default=0).

| sdtv_mode | result |
| --- | --- |
| 0 | Normal NTSC |
| 1 | Japanese version of NTSC – no pedestal |
| 2 | Normal PAL |
| 3 | Brazilian version of PAL – 525/60 rather than 625/50, different subcarrier |

```sdtv_aspect``` defines the aspect ratio for composite output (default=1).

| sdtv_mode | result |
| --- | --- |
| 1 | 4:3 |
| 2 | 14:9 |
| 3 | 16:9 |

```sdtv_disable_colourburst``` disables colour burst on composite output. The picture will be monochrome, but possibly sharper.
 sdtv_disable_colourburst=1  colour burst is disabled.

```hdmi_safe``` Use "safe mode" settings to try to boot with maximum HDMI compatibility. This is the same as the combination of: hdmi_force_hotplug=1, hdmi_ignore_edid=0xa5000080, config_hdmi_boost=4, hdmi_group=2, hdmi_mode=4, disable_overscan=0, overscan_left=24, overscan_right=24, overscan_top=24, overscan_bottom=24
  hdmi_safe=1

```hdmi_ignore_edid``` Enables the ignoring of EDID/display data if your display doesn't have an accurate EDID.
  hdmi_ignore_edid=0xa5000080

```hdmi_edid_file``` when set to 1, will read the EDID data from the edid.dat file instead of from the monitor.<ref name=hdmi_edid_file>http://www.raspberrypi.org/phpBB3/viewtopic.php?p=173430#p173430</ref>
 hdmi_edid_file=1

```hdmi_force_edid_audio``` Pretends all audio formats are supported by display, allowing passthrough of DTS/AC3 even when not reported as supported.
  hdmi_force_edid_audio=1

```hdmi_ignore_edid_audio``` Pretends all audio formats are unsupported by display. This means ALSA will default to analogue.
  hdmi_ignore_edid_audio=1

```hdmi_force_edid_3d``` Pretends all CEA modes support 3D, even when EDID doesn't indicate support for them.
  hdmi_force_edid_3d=1

```avoid_edid_fuzzy_match``` Avoid fuzzy matching of modes described in EDID. Picks the standard mode with matching resolution and closest framerate even if blanking is wrong.
  avoid_edid_fuzzy_match=1

```hdmi_ignore_cec_init``` Doesn't sent initial active source message. Avoids bringing (CEC enabled) TV out of standby and channel switch when rebooting.
  hdmi_ignore_cec_init=1

```hdmi_ignore_cec``` Pretends CEC is not supported at all by TV. No CEC functions will be supported.
  hdmi_ignore_cec=1

```hdmi_force_hotplug``` Pretends HDMI hotplug signal is asserted so it appears a HDMI display is attached.
  hdmi_force_hotplug=1 Use HDMI mode even if no HDMI monitor is detected.

```hdmi_ignore_hotplug``` Pretends HDMI hotplug signal is not asserted so it appears a HDMI display is not attached.
  hdmi_ignore_hotplug=1 Use composite mode even if HDMI monitor is detected.

```hdmi_pixel_encoding``` Force the pixel encoding mode. By default it will use the mode requested from EDID so shouldn't need changing.

| hdmi_pixel_encoding | result |
| --- | --- |
| 0 | RGB limited (16-235) |
| 1 | RGB full (0-255) |
| 2 | YCbCr limited (16-235) |
| 3 | YCbCr full (0-255) |

```hdmi_drive``` chooses between HDMI and DVI modes

| hdmi_drive | result |
| --- | --- |
| 1 | Normal DVI mode (No sound) |
| 2 | Normal HDMI mode (Sound will be sent if supported and enabled) |

```hdmi_group``` defines the HDMI type

Not specifying the group, or setting to 0 will use the preferred group reported by the EDID.

| hdmi_group | result |
| --- | --- |
| 0 | Auto-detect from EDID |
| 1 | CEA |
| 2 |  DMT |

```hdmi_mode``` defines screen resolution in CEA or DMT format.
(For other modes not listed here have a look at [this thread](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=24679).)

 ```These values are valid if hdmi_group=1 (CEA)```
 
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

 In the table above the 16:9 aspect rations are a variant of a mode which usually has 4:3 aspect ratio.
 Pixel doubling and quadrupling indicates a higher clock rate, with each pixel repeated two or four times respectively.

 ```These values are valid if hdmi_group=2 (DMT)```
 Note: according to http://www.raspberrypi.org/phpBB3/viewtopic.php?f=26&t=20155&p=195417&hilit=2560x1600#p195443 
 there is a pixel clock limit which means the highest supported mode is 1920x1200 @60Hz with reduced blanking.

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

```overscan_left```	 number of pixels to skip on left.

```overscan_right```	 number of pixels to skip on right.

```overscan_top```	 number of pixels to skip on top.

```overscan_bottom```	 number of pixels to skip on bottom.

```framebuffer_width```	 console framebuffer width in pixels. Default is display width minus overscan.

```framebuffer_height```	 console framebuffer height in pixels. Default is display height minus overscan.

```framebuffer_depth```	 console framebuffer depth in bits per pixel. Default is 16.  8bit is valid, but default RGB palette makes an unreadable screen. 24bit looks better but has corruption issues as of 20120615. 32bit has no corruption issues but needs framebuffer_ignore_alpha=1 and shows the wrong colors as of 20120615.

```framebuffer_ignore_alpha``` set to 1 to disable alpha channel. Helps with 32bit.

```test_mode```	 enable test sound/image during boot for manufacturing test.

```disable_overscan```	 set to 1 to disable overscan.

```config_hdmi_boost```		configure the signal strength of the HDMI interface. Default is 0. Try 4 if you have interference issues with hdmi. 7 is the maximum.

```display_rotate``` rotates the display clockwise on the screen (default=0) or flips the display.
 display_rotate=0        Normal
 display_rotate=1        90 degrees
 display_rotate=2        180 degrees
 display_rotate=3        270 degrees
 display_rotate=0x10000  horizontal flip
 display_rotate=0x20000  vertical flip

Note: the 90 and 270 degrees rotation options require additional memory on GPU, so won't work with the 16M GPU split. Probably the reason for:
* Crashes my RPI before Linux boots if set to "1" -- REW 20120913.

##Which values are valid for my monitor?
Your HDMI monitor may support only a limited set of formats. To find out which formats are supported, use the following method:

*Set the output format to VGA 60Hz (hdmi_group=1 hdmi_mode=1) and boot up the Raspberry Pi.
*Enter the following command to give a list of CEA supported modes:
 ```/opt/vc/bin/tvservice -m CEA```
*Enter the following command to give a list of DMT supported modes:
 ```/opt/vc/bin/tvservice -m DMT```
*Enter the following command to show your current state:
 ```/opt/vc/bin/tvservice -s```
*Enter the following commands to dump more detailed information from your monitor:
 ```/opt/vc/bin/tvservice -d edid.dat```
 ```/opt/vc/bin/edidparser edid.dat```
The edid.dat should also be provided when troubleshooting problems with the default HDMI mode.

#Licensed codecs
Hardware decoding of additional codecs can be enabled by [purchasing a licence](http://swag.raspberrypi.org/collections/software) that is locked to the CPU serial number of your Raspberry Pi.

```decode_MPG2``` Licence key to allow hardware MPEG-2 decoding.
  decode_MPG2=0x12345678

```decode_WVC1``` Licence key to allow hardware VC-1 decoding.
  decode_WVC1=0x12345678

Licence setup for SD-card sharing between multiple Pis. There is a maximum of eight licences at once.
  decode_XXXX=0x12345678,0xabcdabcd,0x87654321,...

#Boot
```disable_commandline_tags``` stop start.elf from filling in ATAGS (memory from 0x100) before launching kernel.

```cmdline```                 (string) command line parameters. Can be used instead of cmdline.txt file.

```kernel```                  (string) alternative name to use when loading kernel. Default "kernel.img".

```kernel_address```          address to load kernel.img file. 

```kernel_old```              (bool) if 1, load kernel at 0x0.

```ramfsfile```               (string) ramfs file to load.

```ramfsaddr```               address to load ramfs file.

```initramfs```               (string address) ramfs file and adress to load it at (it's like ramfsfile+ramfsaddr in one option). NOTE: this option uses different syntax than all other options - you should not use "=" character here. Example:
 initramfs initramf.gz 0x00800000

```device_tree_address```     address to load device_tree.

```init_uart_baud```          initial uart baud rate. Default 115200.

```init_uart_clock```         initial uart clock. Default 3000000 (3Mhz).

```init_emmc_clock```         initial emmc clock. Default 100000000 (100MHz).

```boot_delay```              wait for given number of seconds in start.elf before loading kernel. delay = 1000 * boot_delay + boot_delay_ms. Default 1.

```boot_delay_ms```           wait for given number of milliseconds in start.elf before loading kernel. Default 0.

```avoid_safe_mode```         if set to 1, [[RPI_safe_mode|safe_mode]] boot won't be enabled. Default 0.

```disable_splash```          if set to 1, avoids the rainbow splash screen on boot.

#Overclocking
```NOTE:``` Setting parameters other than that available by 'raspi-config' will set a permanent bit within the SOC, making it possible to detect that you Pi has been overclocked. This was originally set to detect a void warranty if the device had been overclocked. Since September 19th 2012 you can overclock your Pi without affecting your warranty<ref>[http://www.raspberrypi.org/archives/2008 Introducing turbo mode: up to 50% more performance for free]</ref>.

The latest kernel has a [http://www.pantz.org/software/cpufreq/usingcpufreqonlinux.html cpufreq] kernel driver with the "ondemand" governor enabled by default. It has no effect if you have no overclock settings.
But when you do, the ARM frequency will vary with processor load.  Non-default values are only used when needed according to the governor. You can adjust the minimum values with the *_min config options or disable dynamic clocking with force_turbo=1. <ref name=cpufreq>http://www.raspberrypi.org/phpBB3/viewtopic.php?p=169726#p169726</ref>

Overclock and overvoltage will be disabled at runtime when the SoC reaches 85°C to cool it down. You should not hit the limit, even with maximum settings at 25°C ambient temperature. <ref name=freq_overheat>http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=11579#p169872</ref>

##Overclocking options

{| cellpadding="2"
!Option !! Description
|- 
!align="right"|arm_freq 
| Frequency of ARM in MHz. Default 700.
|- 
!align="right"|gpu_freq 
| Sets core_freq, h264_freq, isp_freq, v3d_freq together. Default 250.
|- 
!align="right"|core_freq 
| Frequency of GPU processor core in MHz. It has an impact on ARM performance since it drives L2 cache. Default 250.
|- 
!align="right"|h264_freq 
| Frequency of hardware video block in MHz. Default 250.
|- 
!align="right"|isp_freq 
| Frequency of image sensor pipeline block in MHz. Default 250.
|- 
!align="right"|v3d_freq 
| Frequency of 3D block in MHz. Default 250.
|- 
!align="right"|avoid_pwm_pll
| Don't dedicate a pll to PWM audio. This will reduce analogue audio quality slightly. The spare PLL allows the core_freq to be set independently from the rest of the gpu allowing more control over overclocking. Default 0.
|- 
!align="right"|sdram_freq 
| Frequency of SDRAM in MHz. Default 400.
|- 
!align="right"|over_voltage 
| ARM/GPU core voltage adjust. [-16,8] equates to [0.8V,1.4V] with 0.025V steps. <ref name=voltages>What this means is that you can specify -16 and get 0.8V as the GPU/core voltage, and specify 8 and get 1.4V</ref> Default is 0 (1.2V). Values above 6 are only allowed when force_turbo or current_limit_override are specified (which set the warranty bit).
|- 
!align="right"|over_voltage_sdram 
| Sets over_voltage_sdram_c, over_voltage_sdram_i, over_voltage_sdram_p together.
|- 
!align="right"|over_voltage_sdram_c 
| SDRAM controller voltage adjust. [-16,8] equates to [0.8V,1.4V] with 0.025V steps. Default 0 (1.2V). <ref name=voltages />
|- 
!align="right"|over_voltage_sdram_i 
| SDRAM I/O voltage adjust. [-16,8] equates to [0.8V,1.4V] with 0.025V steps. Default 0 (1.2V).<ref name=voltages />
|- 
!align="right"|over_voltage_sdram_p 
| SDRAM phy voltage adjust. [-16,8] equates to [0.8V,1.4V] with 0.025V steps. Default 0 (1.2V).<ref name=voltages />
|- 
!align="right"|force_turbo
| Disables dynamic cpufreq driver and minimum settings below. Enables h264/v3d/isp overclock options. Default 0. May set warranty bit.
|- 
!align="right"|initial_turbo
| Enables turbo mode from boot for the given value in seconds (up to 60) or until cpufreq sets a frequency. Can help with SD card corruption if overclocked. Default 0 <ref name=initial_turbo>http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=6201&start=425#p180099</ref>
|- 
!align="right"|arm_freq_min
| Minimum value of arm_freq used for dynamic clocking. Default 700.
|- 
!align="right"|core_freq_min
| Minimum value of core_freq used for dynamic clocking. Default 250.
|- 
!align="right"|sdram_freq_min
| Minimum value of sdram_freq used for dynamic clocking. Default 400.
|- 
!align="right"|over_voltage_min
| Minimum value of over_voltage used for dynamic clocking. Default 0.
|- 
!align="right"|temp_limit
| Overheat protection. Sets clocks and voltages to default when the SoC reaches this Celsius value. Setting this higher than default voids your warranty. Default 85.
|- 
!align="right"| current_limit_override
| Disables SMPS current limit protection when set to "0x5A000020". Can help if you are currently hitting a reboot failure when overclocking too high. May set warranty bit.<ref name=current_limit_override>http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=6201&start=325#p170793</ref>
|}

###force_turbo mode
  force_turbo=0
Enables dynamic clocks and voltage for the ARM core, GPU core and SDRAM. 
When busy, ARM frequency go up to "arm_freq" and down to "arm_freq_min" on idle. 
"core_freq", "sdram_freq" and "over_voltage" behave the same. "over_voltage" is limited to 6 (1.35V).
Non-default values for the h264/v3d/isp parts are ignored.
  force_turbo=1
disables dynamic clocking, so all frequencies and voltages stay high. 
Overclocking of h264/v3d/isp GPU parts is allowed as well as setting "over_voltage" to 8 (1.4V).
<ref name=force_turbo>http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=6201&sid=852d546291ae711ffcd8bf23d3214581&start=325#p170793</ref>

##Clocks relationship

The GPU core, h264, v3d and ISP share a PLL, therefore need to have related frequencies. ARM, SDRAM and GPU each have their own PLLs and can have unrelated frequencies.<ref name=freq_relationship>http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=6201&start=275#p168042</ref> 

The following is not necessary with "avoid_pwm_pll=1".

 pll_freq = floor(2400 / (2 * core_freq)) * (2 * core_freq)
 gpu_freq = pll_freq / [even number]

The effective gpu_freq is automatically rounded to nearest even integer, so asking for core_freq=500 and gpu_freq=300 will result in divisor of 2000/300 = 6.666 => 6 and so 333.33MHz.

##Tested values
The following table shows some successful attempts at overclocking, which can be used for orientation. These settings may not work on every device, and can shorten the lifespan of the Broadcom SoC. 

{| border="1"
! arm_freq !! gpu_freq !! core_freq !! h264_freq !! isp_freq !! v3d_freq !! sdram_freq !! over_voltage !! over_voltage_sdram
|-
|800 || || || || || || || ||
|-
|900 ||275 || || || || ||500 || || 
|-
|900 || ||450 || || || ||450 || || 
|-
|930 ||350 || || || || ||500 || || 
|-
|1000 || ||500 || || || ||500 ||6 ||
|-
|1050 || || || || || || ||6 || 
|-
|1150 || ||500 || || || ||600 ||8 ||
|}
There are [http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=6201&p=159188&hilit=hynix#p159160 reports] that Hynix RAM is not as good as Samsung RAM for overclocking.


##Monitoring Temperature and Voltage 

To monitor the Pi's temperature, look at:  <code>/sys/class/thermal/thermal_zone0/temp</code>.<br>
To monitor the Pi's current frequency, look at: <code>/sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq</code>.<br>
To monitor the Pi's PSU voltage, you'll need a multimeter, to measure across the power supply test points, or the expansion header.

It's generally a good idea to keep the core temp below 70 degrees, and the voltage above 4.8V. (Note that some, not necessarily cheap, USB power supplies fall as low as 4.2V; this is because they are usually designed to charge a 3.7V LiPo battery, rather than to supply a solid 5V to a computer). A heatsink can be helpful, especially if the Pi is to be run inside a case. A suitable heatsink is the self-adhesive BGA (ball-grid-array) 14x14x10 mm heatsink, part 674-4756 from RS Components.

##Overclock stability test

Most overclocking issues show up right away with a failure to boot, but it is possible to get filesystem corruption that arises over time. Here is a script to stress-test the stability of the system, specifically the SD card. If this script runs to completion without any errors showing in <code>dmesg</code>, then the Pi is probably stable with your chosen settings. 

If the system ''does'' crash, then hold down the ''shift'' key during boot, which will temporarily disable all overclocking. Also, note that SD card issues are usually affected by the core_freq, rather than the arm_freq, and that there is a surprisingly big jump in this (from 250 MHz to 500 MHz) between the ''High'' speed (950 MHz) and ''Turbo'' (1 GHz) presets in raspi-config.

 #!/bin/bash
 #Simple stress test for system. If it survives this, it's probably stable.
 #Free software, GPL2+
 
 echo "Testing overclock stability..."
 
 #Max out the CPU in the background (one core). Heats it up, loads the power-supply. 
 nice yes >/dev/null &
 
 #Read the entire SD card 10x. Tests RAM and I/O
 for i in `seq 1 10`; do echo reading: $i; sudo dd if=/dev/mmcblk0 of=/dev/null bs=4M; done
 
 #Writes 512 MB test file,  10x.
 for i in `seq 1 10`; do echo writing: $i; dd if=/dev/zero of=deleteme.dat bs=1M count=512; sync; done
 
 #Clean up
 killall yes
 rm deleteme.dat
 
 #Print summary. Anything nasty will appear in dmesg.
 echo -n "CPU freq: " ; cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
 echo -n "CPU temp: " ; cat /sys/class/thermal/thermal_zone0/temp
 dmesg | tail 
 
 echo "Not crashed yet, probably stable."

____

Thanks to eLinux.org

