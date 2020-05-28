## Frequency management and thermal control

All Raspberry Pi models perform a degree of thermal management to avoid overheating under heavy load. The SoCs have an internal temperature sensor, which software on the GPU polls to ensure that temperatures do not exceed a predefined limit; this is 85°C on all models. It is possible to set this to a lower value, but not to a higher one. As the device approaches the limit, various frequencies and sometimes voltages used on the chip (ARM, GPU) are reduced. This reduces the amount of heat generated, keeping the temperature under control.

When the core temperature is between 80°C and 85°C, a warning icon showing a red half-filled thermometer will be displayed, and the ARM cores will be progressively throttled back. If the temperature reaches 85°C, an icon showing a fully filled thermometer will be displayed, and both the ARM cores and the GPU will be throttled back. See the page on [warning icons](../../configuration/warning-icons.md) for images of the icons.

For Raspberry Pi 3 Model B+, the PCB technology has been changed to provide better heat dissipation and increased thermal mass. In addition, a soft temperature limit has been introduced, with the goal of maximising the time for which a device can "sprint" before reaching the hard limit at 85°C. When the soft limit is reached, the clock speed is reduced from 1.4GHz to 1.2GHz, and the operating voltage is reduced slightly. This reduces the rate of temperature increase: we trade a short period at 1.4GHz for a longer period at 1.2GHz. By default, the soft limit is 60°C, and this can be changed via the `temp_soft_limit` setting in [config.txt](../../configuration/config-txt/overclocking.md).

The Raspberry Pi 4 Model B continues with the same PCB technology as the Raspberry Pi 3B+ to help dissipate excess heat. There is currently no soft limit defined.

### DVFS on the Raspberry Pi 4B

On Raspberry Pi 4 Model B, firmware from late November 2019 onwards implements Dynamic Voltage and Frequency Scaling. This technique (outlined on Wikipedia [here](https://en.wikipedia.org/wiki/Dynamic_voltage_scaling)) allows Raspberry Pi 4B to run at lower temperatures whilst still providing the same performance.

Various clocks (e.g. ARM, Core, V3D, ISP, H264, HEVC) inside the SoC are monitored by the firmware, and whenever they are not running at full speed, the voltage supplied to the particular part of the chip driven by the clock is reduced relative to the reduction from full speed. In effect, only enough voltage is supplied to keep the block running correctly at the specific speed at which it is running. This can result in significant reductions in power used by the SoC, and therefore in the overall heat being produced.

In addition, a more stepped CPU governor is also used to produce finer-grained control of ARM core frequencies, which means the DVFS is more effective. The steps are now 1500MHz, 1000MHz, 750MHz, and 600MHz. These steps can also help when the SoC is being throttled, and mean that throttling all the way back to 600MHz is much less likely, giving an overall increase in fully loaded performance.

### Heatsinks

Whilst heatsinks are not necessary to prevent overheating damage to the SoC (the thermal throttling mechanism handles that), a heatsink or small fan will help if you wish to reduce the amount of thermal throttling that takes place. Depending on the exact circumstances, mounting the Pi vertically can also help with heat dissipation, as doing so can improve air flow.

### Measuring temperature

Due to the architecture of the SoCs used on the Raspberry Pi range, and the use of the upstream temperature monitoring code in the Raspberry Pi OS distribution, Linux-based temperature measurements can be inaccurate. There is a command that can provide an accurate and instantaneous reading of the current SoC temperature, as it communicates with the GPU directly:

```vcgencmd measure_temp```
