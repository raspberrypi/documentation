## config.txt - Overclocking options

**NOTE:** Setting any overclocking parameters to values other than those used by [raspi-config](../raspi-config.md#overclock) will set a permanent bit within the SoC, making it possible to detect that your Pi has been overclocked. This was originally set to detect a void warranty if the device had been overclocked. Since September 19th 2012, you can overclock your Pi without affecting your warranty. For more information see the [blog post on Turbo Mode](https://www.raspberrypi.org/blog/introducing-turbo-mode-up-to-50-more-performance-for-free/).

The latest kernel has a [cpufreq](http://www.pantz.org/software/cpufreq/usingcpufreqonlinux.html) kernel driver with the "ondemand" governor enabled by default. It has no effect if you have no overclock settings, but if you overclock, the CPU frequency will vary with processor load. Non-default values are only used when required, according to the governor. You can adjust the minimum values with the `*_min` config options, or disable dynamic clocking with `force_turbo=1`. For more information [see here](http://www.raspberrypi.org/phpBB3/viewtopic.php?p=169726#p169726).

Overclocking and overvoltage will be disabled at runtime when the SoC reaches 85°C, in order to cool it down. You should not hit this limit, even with maximum settings at 25°C ambient temperature. For more information [see here](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=11579#p169872).

### Overclocking options

| Option | Description |
| --- | --- |
| arm_freq | Frequency of the ARM CPU in MHz. The default value is `700`. |
| gpu_freq | Sets `core_freq`, `h264_freq`, `isp_freq`, and `v3d_freq` together. The default value is `250`. |
| core_freq | Frequency of the GPU processor core in MHz. It has an impact on CPU performance because it drives the L2 cache. The default value is `250`. |
| h264_freq | Frequency of the hardware video block in MHz. The default value is `250`. |
| isp_freq | Frequency of the image sensor pipeline block in MHz. The default value is `250`. |
| v3d_freq | Frequency of the 3D block in MHz. The default value is `250`. |
| sdram_freq | Frequency of the SDRAM in MHz. The default value is `400`. |
| over_voltage | CPU/GPU core voltage adjustment. [-16,8] equates to [0.8V,1.4V] with 0.025V steps. In other words, specifying -16 will give 0.8V as the GPU/core voltage, and specifying 8 will give 1.4V. The default value is `0` (1.2V). Values above 6 are only allowed when `force_turbo` or `current_limit_override` are specified: this sets the warranty bit. |
| over_voltage_sdram | Sets `over_voltage_sdram_c`, `over_voltage_sdram_i`, and `over_voltage_sdram_p` together. |
| over_voltage_sdram_c | SDRAM controller voltage adjustment. [-16,8] equates to [0.8V,1.4V] with 0.025V steps. The default value is `0` (1.2V). |
| over_voltage_sdram_i | SDRAM I/O voltage adjustment. [-16,8] equates to [0.8V,1.4V] with 0.025V steps. The default value is `0` (1.2V). |
| over_voltage_sdram_p | SDRAM phy voltage adjustment. [-16,8] equates to [0.8V,1.4V] with 0.025V steps. The default value is `0` (1.2V). |
| force_turbo | Disables the dynamic cpufreq driver and minimum settings described below. Enables h264/v3d/isp overclocking options. The default value is `0`. Enabling this may set the warranty bit. |
| initial_turbo | Enables turbo mode from boot for the given value in seconds up to 60, or until cpufreq sets a frequency. For more information [see here](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=6201&start=425#p180099). This option can help with SD card corruption if the Pi is overclocked. The default value is `0`. |
| arm_freq_min | Minimum value of `arm_freq` used for dynamic frequency clocking. The default value is `700`. |
| core_freq_min | Minimum value of `core_freq` used for dynamic frequency clocking. The default value is `250`. |
| sdram_freq_min | Minimum value of `sdram_freq` used for dynamic frequency clocking. The default value is `400`. |
| over_voltage_min | Minimum value of `over_voltage` used for dynamic frequency clocking. The default value is `0`. |
| temp_limit | Overheat protection. This sets the clocks and voltages to default when the SoC reaches this value in Celsius. Setting this higher than the default voids your warranty. The default value is `85`. |
| current_limit_override | Disables SMPS current limit protection when set to `0x5A000020`. It requires this unusual value to ensure that it is not triggered accidentally. This can help if you are hitting a reboot failure when specifying a value for overclocking that is too high. For more information [see here](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=6201&start=325#p170793). Changing this option may set the warranty bit. |

#### force_turbo

`force_turbo=0`

This enables dynamic clocks and voltage for the CPU, GPU core, and SDRAM. The CPU frequency goes up to `arm_freq` when busy, and down to `arm_freq_min` on idle.

`core_freq`/`core_freq_min`, `sdram_freq`/`sdram_freq_min` and `over_voltage`/`over_voltage_min` behave in a similar manner. `over_voltage` is limited to 6 (1.35V). Non-default values for the h264/v3d/isp frequencies are ignored.

`force_turbo=1`

Disables dynamic frequency clocking, so that all frequencies and voltages stay high. Overclocking of h264/v3d/isp GPU parts is allowed, as well as setting `over_voltage` up to 8 (1.4V). For more information [see here](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=6201&sid=852d546291ae711ffcd8bf23d3214581&start=325#p170793).

### Clocks relationship

The GPU core, h264, v3d, and ISP blocks all share a [PLL](https://en.wikipedia.org/wiki/Phase-locked_loop#Clock_generation) and therefore need to have related frequencies. The CPU, SDRAM and GPU each have their own PLLs and can have unrelated frequencies. For more information [see here](http://www.raspberrypi.org/phpBB3/viewtopic.php?f=29&t=6201&start=275#p168042).

The frequencies are calculated as follows:

```
pll_freq = floor(2400 / (2 x core_freq)) x (2 x core_freq)
gpu_freq = pll_freq / [even number]
```

The effective `gpu_freq` is automatically rounded to the nearest even integer; asking for `core_freq=500` and `gpu_freq=300` will result in the divisor of 2000/300 = 6.666 => 6 and so result in a `gpu_freq` of 333.33MHz.

### Monitoring temperature and voltage

To view the Pi's temperature, type: `cat /sys/class/thermal/thermal_zone0/temp`. Divide the result by 1000 to find the value in Celsius.

To view the Pi's current frequency, type: `cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq`. Divide the result by 1000 to find the value in MHz.

To monitor the Pi's PSU voltage, you will need to use a multimeter to measure between the TP1 and TP2 power supply test points. More information is available in [power](../../hardware/raspberrypi/power/README.md).

It is a good idea to keep the core temperature below 70 degrees and the voltage above 4.8V. Note that some USB power supplies fall as low as 4.2V. This is because they are usually designed to charge a 3.7V LiPo battery, rather than to supply 5V to a computer. If your overclocked Raspberry Pi is getting hot, a heatsink can be helpful, especially if the Pi is to be run inside a case. A suitable heatsink is the self-adhesive BGA (ball-grid-array) 14x14x10 mm heatsink, available from [RS Components](http://uk.rs-online.com/web/p/heatsinks/6744756/).

### Overclocking problems

Most overclocking issues show up immediately with a failure to boot. If this occurs, hold down the `shift` key during the next boot. This will temporarily disable all overclocking, allowing you to boot successfully and then edit your settings.




*This article uses content from the eLinux wiki page [RPiconfig](http://elinux.org/RPiconfig), which is shared under the [Creative Commons Attribution-ShareAlike 3.0 Unported license](http://creativecommons.org/licenses/by-sa/3.0/)*
