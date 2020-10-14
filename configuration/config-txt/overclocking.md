# Overclocking options in config.txt

**NOTE:** Setting any overclocking parameters to values other than those used by [raspi-config](../raspi-config.md#overclock) may set a permanent bit within the SoC, making it possible to detect that your Pi has been overclocked. The specific circumstances where the overclock bit is set are if `force_turbo` is set to `1` and any of the `over_voltage_*` options are set to a value > `0`. See the [blog post on Turbo Mode](https://www.raspberrypi.org/blog/introducing-turbo-mode-up-to-50-more-performance-for-free/) for more information. **Pi 4** overclocking options may be subject to change in the future.

The latest kernel has a [cpufreq](http://www.pantz.org/software/cpufreq/usingcpufreqonlinux.html) kernel driver with the "ondemand" governor enabled by default. It has no effect if you have no overclock settings, but if you overclock, the CPU frequency will vary with processor load. Non-default values are only used when required, according to the governor. You can adjust the minimum values with the `*_min` config options (only values lower than default are applied) or disable dynamic clocking (and force overclocking) with `force_turbo=1`. For more information [see this section of the documentation](../../hardware/raspberrypi/frequency-management.md).

Overclocking and overvoltage will be disabled at runtime when the SoC reaches 85°C, in order to cool the SoC down. You should not hit this limit with Raspberry Pi Models 1 or 2, but you are more likely to with Raspberry Pi 3 and Raspberry Pi 4B. For more information [see this section of the documentation](../../hardware/raspberrypi/frequency-management.md). Overclocking and overvoltage are also disabled when an undervoltage situation is detected.

## Overclocking options

| Option | Description |
| --- | --- |
| arm_freq | Frequency of the ARM CPU in MHz. |
| gpu_freq | Sets `core_freq`, `h264_freq`, `isp_freq`, `v3d_freq` and `hevc_freq` together |
| core_freq | Frequency of the GPU processor core in MHz, influences CPU performance because it drives the L2 cache and memory bus; the L2 cache benefits only Pi Zero/Pi Zero W/ Pi 1, there is a small benefit for SDRAM on Pi 2/Pi 3. See section below for use on the Pi 4.|
| h264_freq | Frequency of the hardware video block in MHz; individual override of the `gpu_freq` setting |
| isp_freq | Frequency of the image sensor pipeline block in MHz; individual override of the `gpu_freq` setting |
| v3d_freq | Frequency of the 3D block in MHz; individual override of the `gpu_freq` setting |
| hevc_freq | Frequency of the High Efficiency Video Codec block in MHz; individual override of the `gpu_freq` setting. Pi 4 only. |
| sdram_freq | Frequency of the SDRAM in MHz. SDRAM overclocking on Pi 4B is not currently supported|
| over_voltage | CPU/GPU core voltage adjustment. The value should be in the range [-16, 8] which equates to the range [0.8V, 1.4V] with 0.025V steps. In other words, specifying -16 will give 0.8V as the GPU/core voltage, and specifying 8 will give 1.4V. For defaults see table below. Values above 6 are only allowed when `force_turbo` is specified: this sets the warranty bit if `over_voltage_*` is also set. |
| over_voltage_sdram | Sets `over_voltage_sdram_c`, `over_voltage_sdram_i`, and `over_voltage_sdram_p` together. |
| over_voltage_sdram_c | SDRAM controller voltage adjustment. [-16,8] equates to [0.8V,1.4V] with 0.025V steps. |
| over_voltage_sdram_i | SDRAM I/O voltage adjustment. [-16,8] equates to [0.8V,1.4V] with 0.025V steps. |
| over_voltage_sdram_p | SDRAM phy voltage adjustment. [-16,8] equates to [0.8V,1.4V] with 0.025V steps. |
| force_turbo | Forces turbo mode frequencies even when the ARM cores are not busy. Enabling this may set the warranty bit if `over_voltage_*` is also set. |
| initial_turbo | Enables turbo mode from boot for the given value in seconds, or until cpufreq sets a frequency. For more information [see here](https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=6201&start=425#p180099). The maximum value is `60`. |
| arm_freq_min | Minimum value of `arm_freq` used for dynamic frequency clocking. |
| core_freq_min | Minimum value of `core_freq` used for dynamic frequency clocking. |
| gpu_freq_min | Minimum value of `gpu_freq` used for dynamic frequency clocking. |
| h264_freq_min | Minimum value of `h264_freq` used for dynamic frequency clocking. |
| isp_freq_min | Minimum value of `isp_freq` used for dynamic frequency clocking. |
| v3d_freq_min | Minimum value of `v3d_freq` used for dynamic frequency clocking. |
| hevc_freq_min | Minimum value of `hevc_freq` used for dynamic frequency clocking. |
| sdram_freq_min | Minimum value of `sdram_freq` used for dynamic frequency clocking. |
| over_voltage_min | Minimum value of `over_voltage` used for dynamic frequency clocking. |
| temp_limit | Overheat protection. This sets the clocks and voltages to default when the SoC reaches this value in Celsius. Values over 85 are clamped to 85. |
| temp_soft_limit | **3A+/3B+ only**. CPU speed throttle control. This sets the temperature at which the CPU clock speed throttling system activates. At this temperature, the clock speed is reduced from 1400MHz to 1200MHz.  Defaults to `60`, can be raised to a maximum of `70`, but this may cause instability. |

This table gives the default values for the options on various Raspberry Pi Models, all frequencies are stated in MHz.

| Option       | Pi 0/W | Pi1 | Pi2 | Pi3   | Pi3A+/Pi3B+ | Pi4  |
| ---          | :---:  | :---: | :---: | :----:  | :-----: | :----: |
| arm_freq     | 1000   | 700 | 900 | 1200  | 1400  | 1500 |
| core_freq    | 400    | 250 | 250 | 400   | 400   | 500/550/360 |
| h264_freq    | 300    | 250 | 250 | 400   | 400   | 500/550/360 |
| isp_freq     | 300    | 250 | 250 | 400   | 400   | 500/550/360 |
| v3d_freq     | 300    | 250 | 250 | 400   | 400   | 500/550/360 |
| hevc_freq    | N/A    | N/A | N/A | N/A   | N/A   | 500/550/360 |
| sdram_freq   | 450    | 400 | 450 | 450   | 500   | 3200 |
| arm_freq_min | 700    | 700 | 600 | 600   | 600   | 600  |
| core_freq_min| 250    | 250 | 250 | 250   | 250   | 250/275 |
| gpu_freq_min | 250    | 250 | 250 | 250   | 250   | 500  |
| h264_freq_min|  250   | 250 | 250 | 250   | 250   | 500  |
| isp_freq_min |  250   | 250 | 250 | 250   | 250   | 500  |
| v3d_freq_min |  250   | 250 | 250 | 250   | 250   | 500  |
| sdram_freq_min |400   | 400 | 400 | 400   | 400   | 400  |

This table gives defaults for options that are the same across all models.

| Option               | Default |
| ---                  | :---:   |
| initial_turbo        | 0       |
| overvoltage_min      | 0       |
| temp_limit           | 85      |
| over_voltage_sdram_c | 0 (1.2V) |
| over_voltage_sdram_i | 0 (1.2V) |
| over_voltage_sdram_p | 0 (1.2V) |

This table lists the default `over_voltage` settings for the various Pi models. The firmware uses Adaptive Voltage Scaling (AVS) to determine the optimum voltage to set. Note that for each integer rise in `over_voltage`, the voltage will be 25mV higher.

| Model | Default | Resulting voltage |
| --- | --- | --- |
| Pi 1 | 0 | 1.2V |
| Pi 2 | 0 | 1.2-1.3125V |
| Pi 3 | 0 | 1.2-1.3125V |
| Pi Zero | 6 | 1.35V |

#### Specific to Pi 4B

The `core_freq` of the Raspberry Pi 4 can change from the default if either `hdmi_enable_4kp60` or `enable_tvout` are used, due to relationship between internal clocks and the particular requirements of the requested display modes.

| Display option | Frequency |
| -------------- | --------: |
| Default        | 500 |
| enable_tvout | 360 |
| hdmi_enable_4kp60 | 550 |

Changing `core_freq` in `config.txt` is not supported on the Pi 4, any change from the default will almost certainly cause a failure to boot.

It is recommended when overclocking to use the individual frequency settings (`isp_freq`, `v3d_freq` etc) rather than `gpu_freq`, as since it attempts to set `core_freq` (which cannot be changed on the Pi 4), it is not likely to have the desired effect.

### force_turbo

By default (`force_turbo=0`) the "On Demand" CPU frequency driver will raise clocks to their maximum frequencies when the ARM cores are busy and will lower them to the minimum frequencies when the ARM cores are idle.

`force_turbo=1` overrides this behaviour and forces maximum frequencies even when the ARM cores are not busy.

### never_over_voltage

Sets a bit in the OTP memory (one time programmable) that prevents the device from being overvoltaged. This is intended to lock the device down so the warranty bit cannot be set either inadvertently or maliciously by using an invalid overvoltage.

### disable_auto_turbo

On Pi 2/Pi 3, setting this flag will disable the GPU from moving into turbo mode, which it can do in particular load cases.

## Clocks relationship

The GPU core, CPU, SDRAM and GPU each have their own PLLs and can have unrelated frequencies. The h264, v3d and ISP blocks share a PLL. For more information [see here](https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=6201&start=275#p168042).

To view the Pi's current frequency in KHz, type: `cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq`. Divide the result by 1000 to find the value in MHz. Note that this frequency is the kernel *requested* frequency, and it is possible that any throttling (for example at high temperatures) may mean the CPU is actually running more slowly than reported. An instantaneous measurement of the actual ARM CPU frequency can be retrieved using the vcgencmd `vcgencmd measure_clock arm`. This is displayed in Hertz.

## Monitoring core temperature

To view the Pi's temperature, type `cat /sys/class/thermal/thermal_zone0/temp`. Divide the result by 1000 to find the value in degrees Celsius. Alternatively, there is a vcgencmd, `vcgencmd measure_temp` that interrogates the GPU directly for its temperature.

Whilst hitting the temperature limit is not harmful to the SoC, it will cause CPU throttling. A heatsink can help to control the core temperature and therefore performance. This is especially useful if the Pi is running inside a case. Airflow over the heatsink will make cooling more efficient.

With firmware from 12th September 2016 or later, when the core temperature is between 80'C and 85'C, a warning icon showing a red half-filled thermometer will be displayed, and the ARM cores will be throttled back. If the temperature exceeds 85'C, an icon showing a fully-filled thermometer will be displayed, and both the ARM cores and the GPU will be throttled back.

For the Raspberry Pi 3 Model B+, the PCB technology has been changed to provide better heat dissipation and increased thermal mass. In addition, a soft temperature limit has been introduced, with the goal of maximising the time for which a device can "sprint" before reaching the hard limit at 85°C. When the soft limit is reached, the clock speed is reduced from 1.4GHz to 1.2GHz, and the operating voltage is reduced slightly. This reduces the rate of temperature increase: we trade a short period at 1.4GHz for a longer period at 1.2GHz. By default, the soft limit is 60°C, and this can be changed via the `temp_soft_limit` setting in config.txt.

See the page on [warning icons](../warning-icons.md) for more details.

## Monitoring voltage

It is essential to keep the supply voltage above 4.8V for reliable performance. Note that the voltage from some USB chargers/power supplies can fall as low as 4.2V. This is because they are usually designed to charge a 3.7V LiPo battery, not to supply 5V to a computer.

To monitor the Pi's PSU voltage, you will need to use a multimeter to measure between the VCC and GND pins on the GPIO. More information is available in [power](../../hardware/raspberrypi/power/README.md).

If the voltage drops below 4.63V (+-5%), recent versions of the firmware will show a yellow lightning bolt symbol on the display to indicate a lack of power, and a message indicating the low voltage state will be added to the kernel log.

See the page on [warning icons](../warning-icons.md) for more details.

## Overclocking problems

Most overclocking issues show up immediately with a failure to boot. If this occurs, hold down the `shift` key during the next boot. This will temporarily disable all overclocking, allowing you to boot successfully and then edit your settings.




*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
