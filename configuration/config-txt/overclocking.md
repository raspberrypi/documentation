# Overclocking options in config.txt

**NOTE:** Setting any overclocking parameters to values other than those used by [raspi-config](../raspi-config.md#overclock) may set a permanent bit within the SoC, making it possible to detect that your Pi has been overclocked. The specific circumstances where the overclock bit is set are if `force_turbo` is set to `1` and any of the `over_voltage_*` options are set to a value > `0`. See the [blog post on Turbo Mode](https://www.raspberrypi.org/blog/introducing-turbo-mode-up-to-50-more-performance-for-free/) for more information. **Pi 4** overclocking options may be subject to change in the future.

The latest kernel has a [cpufreq](http://www.pantz.org/software/cpufreq/usingcpufreqonlinux.html) kernel driver with the "ondemand" governor enabled by default. It has no effect if you have no overclock settings, but if you overclock, the CPU frequency will vary with processor load. Non-default values are only used when required, according to the governor. You can adjust the minimum values with the `*_min` config options (only values lower than default are applied) or disable dynamic clocking (and force overclocking) with `force_turbo=1`. For more information [see this section of the documentation](../../hardware/raspberrypi/frequency-management.md).

Overclocking and overvoltage will be disabled at runtime when the SoC reaches 85°C, in order to cool the SoC down. You should not hit this limit with Raspberry Pi Models 1 or 2, but you are more likely to with Raspberry Pi 3 and Raspberry Pi 4B. For more information [see this section of the documentation](../../hardware/raspberrypi/frequency-management.md). Overclocking and overvoltage are also disabled when an undervoltage situation is detected.

## Overclocking options

| Option | Description |
| --- | --- |
| arm_freq | Frequency of the ARM CPU in MHz; default value is `1000` for Pi Zero and Pi Zero W, `700` for Pi 1, `900` for Pi 2, `1200` for Pi 3, `1400` for Pi 3A+/3B+, `1500` for Pi 4B|
| gpu_freq | Sets `core_freq`, `h264_freq`, `isp_freq`, and `v3d_freq` together; on Pi 1/Pi 2, the default value is `250` for all items, on Pi 3/Pi Zero /Pi Zero W `core_freq` defaults to `400`, while `h264_freq`, `isp_freq`, and `v3d_freq`default to `300`; on Pi 4B the `core_freq`, `h264_freq`, `isp_freq`, and `v3d_freq` default to `500`, `600` is the only other accepted value|
| core_freq | Frequency of the GPU processor core in MHz, influences CPU performance because it drives the L2 cache and memory bus; default value is `250` for Pi 1/Pi 2 and `400` for Pi 3/Pi Zero/Pi Zero W. For Pi 4B the default value is `500`, `600` is the only other accepted value; the L2 cache benefits only Pi Zero/Pi Zero W/ Pi 1, there is a small benefit for SDRAM on Pi 2/Pi 3 and Pi 4B|
| h264_freq | Frequency of the hardware video block in MHz; individual override of the `gpu_freq` setting |
| isp_freq | Frequency of the image sensor pipeline block in MHz; individual override of the `gpu_freq` setting |
| v3d_freq | Frequency of the 3D block in MHz; individual override of the `gpu_freq` setting |
| sdram_freq | Frequency of the SDRAM in MHz; default value is `400` on Pi 1/Pi 2, `450` on Pi 3/Pi Zero/Pi Zero W, `500` on Pi 3A+/3B+, `3200` on Pi 4B. SDRAM overclocking on Pi 4B is not currently supported|
| over_voltage | CPU/GPU core voltage adjustment. [-16,8] equates to [0.8V,1.4V] with 0.025V steps. In other words, specifying -16 will give 0.8V as the GPU/core voltage, and specifying 8 will give 1.4V. For defaults see table below. Values above 6 are only allowed when `force_turbo` is specified: this sets the warranty bit if `over_voltage_*` is also set. |
| over_voltage_sdram | Sets `over_voltage_sdram_c`, `over_voltage_sdram_i`, and `over_voltage_sdram_p` together. |
| over_voltage_sdram_c | SDRAM controller voltage adjustment. [-16,8] equates to [0.8V,1.4V] with 0.025V steps. The default value is `0` (1.2V). |
| over_voltage_sdram_i | SDRAM I/O voltage adjustment. [-16,8] equates to [0.8V,1.4V] with 0.025V steps. The default value is `0` (1.2V). |
| over_voltage_sdram_p | SDRAM phy voltage adjustment. [-16,8] equates to [0.8V,1.4V] with 0.025V steps. The default value is `0` (1.2V). |
| force_turbo | Forces turbo mode frequencies even when the ARM cores are not busy. Enabling this may set the warranty bit if `over_voltage_*` is also set. |
| initial_turbo | Enables turbo mode from boot for the given value in seconds, or until cpufreq sets a frequency. For more information [see here](https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=6201&start=425#p180099). The default value is `0`, maximum value is `60`. |
| arm_freq_min | Minimum value of arm_freq used for dynamic frequency clocking. The default value is `700` for Pi Zero/Pi 1, `600` for Pi 2/Pi 3. |
| core_freq_min | Minimum value of `core_freq` used for dynamic frequency clocking. The default value is `250`. On Pi 4B the default is`275` when `hdmi_enable_4kp60` is set|
| gpu_freq_min | Minimum value of `gpu_freq` used for dynamic frequency clocking. The default value is `250`, or `500` on Pi 4B. |
| h264_freq_min | Minimum value of `h264_freq` used for dynamic frequency clocking. The default value is `250`, or `500` on Pi 4B. |
| isp_freq_min | Minimum value of `isp_freq` used for dynamic frequency clocking. The default value is `250`, or `500` on Pi 4B. |
| v3d_freq_min | Minimum value of `v3d_freq` used for dynamic frequency clocking. The default value is `250`, or `500` on Pi 4B. |
| sdram_freq_min | Minimum value of `sdram_freq` used for dynamic frequency clocking. The default value is `400`. |
| over_voltage_min | Minimum value of `over_voltage` used for dynamic frequency clocking. The default value is `0`. |
| temp_limit | Overheat protection. This sets the clocks and voltages to default when the SoC reaches this value in Celsius.  The default value is `85`. Values over 85 are clamped to 85.|
| temp_soft_limit | **3A+/3B+ only**. CPU speed throttle control. This sets the temperature at which the CPU clock speed throttling system activates. At this temperature, the clock speed is reduced from 1400Mhz to 1200Mhz.  Defaults to `60`, can be raised to a maximum of `70`, but this may cause instability.

This table describes the overvoltage settings for the various Pi models. The firmware uses Adaptive Voltage Scaling (AVS) to determine the optimum voltage to set. Note that for each integer rise in over_voltage, the voltage will be 25mV higher.

| Version | Default overvoltage | Setting |
| --- | --- | --- |
| Pi 1 | 1.2V | 0 |
| Pi 2 | 1.2-1.3125V | 0 |
| Pi 3 | 1.2-1.3125V | 0 |
| Pi Zero | 1.35V | 6 |

**Specific to Pi 4B**: The `core_freq` of the Raspberry Pi 4 can change from the default if either `hdmi_enable_4kp60` or `enable_tvout` are used, due to relationship between internal clocks and the particular requirements of the requested display modes.

|Display option | Frequency |
|---------------|-----------|
| Default        | 500 |     
| enable_tvout | 432 |
| hdmi_enable_4kp60 | 600 |

### force_turbo

By default (`force_turbo=0`) the "On Demand" CPU frequency driver will raise clocks to their maximum frequencies when the ARM cores are busy and will lower them to the minimum frequencies when the ARM cores are idle.

`force_turbo=1` overrides this behaviour and forces maximum frequencies even when the ARM cores are not busy.

### never_over_voltage

Sets a bit in the OTP memory (one time programmable) that prevents the device from being overvoltaged. This is intended to lock the device down so the warranty bit cannot be set either inadvertently or maliciously by using an invalid overvoltage.

### disable_auto_turbo

On Pi 2/Pi 3, setting this flag will disable the GPU from moving into turbo mode, which it can do in particular load cases.

## Clocks relationship

The GPU core, CPU, SDRAM and GPU each have their own PLLs and can have unrelated frequencies. The h264, v3d and ISP blocks share a PLL. For more information [see here](https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=6201&start=275#p168042).

To view the Pi's current frequency, type: `cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq`. Divide the result by 1000 to find the value in MHz. Note that this frequency is the kernel *requested* frequency, and it is possible that any throttling (for example at high temperatures) may mean the CPU is actually running more slowly than reported. An instantaneous measurement of the actual ARM CPU frequency can be retrieved using the vcgencmd `vcgencmd measure_clock arm`. This is displayed in Hertz.

## Monitoring core temperature

To view the Pi's temperature, type `cat /sys/class/thermal/thermal_zone0/temp`. Divide the result by 1000 to find the value in degrees Celsius. Alternatively, there is a vcgencmd, `vcgencmd measure_temp` that interrogates the GPU directly for its temperature.

Whilst hitting the temperature limit is not harmful to the SoC, it will cause CPU throttling. A heatsink can help to control the core temperature and therefore performance. This is especially useful if the Pi is running inside a case. Airflow over the heatsink will make cooling more efficient. A suitable heatsink is the self-adhesive BGA (ball-grid-array) 14x14x10 mm heatsink available from [RS Components](http://uk.rs-online.com/web/p/heatsinks/6744756/).

With firmware from 12th September 2016 or later, when the core temperature is between 80'C and 85'C, a warning icon showing a red half-filled thermometer will be displayed, and the ARM cores will be throttled back. If the temperature exceeds 85'C, an icon showing a fully-filled thermometer will be displayed, and both the ARM cores and the GPU will be throttled back.

For the Raspberry Pi 3 Model B+, the PCB technology has been changed to provide better heat dissipation and increased thermal mass. In addition, a soft temperature limit has been introduced, with the goal of maximising the time for which a device can "sprint" before reaching the hard limit at 85°C. When the soft limit is reached, the clock speed is reduced from 1.4GHz to 1.2GHz, and the operating voltage is reduced slightly. This reduces the rate of temperature increase: we trade a short period at 1.4GHz for a longer period at 1.2GHz. By default, the soft limit is 60°C, and this can be changed via the temp_soft_limit setting in config.txt.

See the page on [warning icons](../warning-icons.md) for more details.

## Monitoring voltage

It is essential to keep the supply voltage above 4.8V for reliable performance. Note that the voltage from some USB chargers/power supplies can fall as low as 4.2V. This is because they are usually designed to charge a 3.7V LiPo battery, not to supply 5V to a computer. 

To monitor the Pi's PSU voltage, you will need to use a multimeter to measure between the VCC and GND pins on the GPIO. More information is available in [power](../../hardware/raspberrypi/power/README.md).

If the voltage drops below 4.63v (+-5%), recent versions of the firmware will show a yellow lightning bolt symbol on the display to indicate a lack of power, and a message indicating the low voltage state will be added to the kernel log.

See the page on [warning icons](../warning-icons.md) for more details.

## Overclocking problems

Most overclocking issues show up immediately with a failure to boot. If this occurs, hold down the `shift` key during the next boot. This will temporarily disable all overclocking, allowing you to boot successfully and then edit your settings.




*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
