## Frequency Management and Thermal control

All Raspberry Pi models perform a degree of thermal management to avoid overheating under heavy load. The SoCs have an internal temperature sensor which software on the GPU polls to ensure that temperatures do not exceed a predefined limit - this limit is 85°C on all models. It is possible set this to a lower value, but not higher. As the device approaches the limit, various frequencies and sometimes voltages used on the chip (ARM, GPU) are reduced. This reduces the amount of heat generated, keeping the temperature under control.

With firmware from 12th September 2016 or later, when the core temperature is between 80°C and 85°C, a warning icon showing a red half-filled thermometer will be displayed, and the ARM cores will be progressively throttled back. If the temperature reaches 85°C, an icon showing a fully-filled thermometer will be displayed, and both the ARM cores and the GPU will be throttled back. See the page on [warning icons](../../configuration/warning-icons.md) for images of the icons.

For Raspberry Pi 3B+, the PCB technology has been changed to provide better heat disipation and increased thermal mass. In addition, a soft temperature limit has been introduced, with the goal of maximising the time for which a device can "sprint" before reaching the hard limit at 85'C. When the soft limit is reached, the clock speed is reduced from 1.4GHz to 1.2GHz, and the operating voltage is reduced slightly. This reduces the rate of temperature increase: we trade a short period at 1.4GHz for a longer period at 1.2GHz. By default the soft limit is 60°C, although this can be changed via the temp_soft_limit setting in [config.txt](../../configuration/config-txt/overclocking.md).. 

### Heatsinks

Whilst heatsinks are not necessary to prevent overheating damage to the SoC (the thermal throttling mechanism handles that), if you wish to reduce the amount of thermal throttling that takes place, a heatsink or small fan will help. Depending on the exact circumstances, mounting the Pi vertically can also help with heat dissipation as airflow can be improved.

### Measuring Temperature

Due to the architecture of the SoCs used on the Raspberry Pi range, and the use in the Raspbian distribtution of the upstream temperature monitoring code, Linux based temperature measurements can be inaccurate. There is a gencmd which can provide an accurate and instantaneous reading of the current SoC temperature, as it communicates with the GPU directly. 

```vcgencmd measure_temp```
