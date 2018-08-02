## Frequency Management and Thermal control

All Raspberry Pi models use some sort of thermal management to ensure the devices do not over heat. The SoC's have an internal thermometer which software on the GPU uses to ensure that temperatures do not exceed a predefined limit - this limit is 85°c on all models. It is possible set this to a lower value, but not higher.

Generally, as the device approaches a limit, various frequencies and sometimes voltages used on the chip (ARM, GPU) are reduced, which means that they produce less heat, and therefor keep the overall temperatures under control.

With firmware from 12th September 2016 or later, when the core temperature is between 80'C and 85'C, a warning icon showing a red half-filled thermometer will be displayed, and the ARM cores will be throttled back. If the temperature exceeds 85'C, an icon showing a fully-filled thermometer will be displayed, and both the ARM cores and the GPU will be throttled back. See the page on [warning icons](../../configuration/warning-icons.md) for images of the icons.

On the Pi3B+, with its higher peak clock speed, the PCB design was changed to provide better heat disipation capabiliies, and to complement this, an additional step has been taken to ensure temperatures stay under control. At a specific temperature, known as the temp_soft_limit, the clock speed is reduced from 1400 to 1200Mhz. By default this limit is 60°c, although this can be changed with an entry in [config.txt](../../configuration/config-txt/overclocking.md). This limit is intended to reduce any large swings in CPU speeds as the high limit is reached, and should give a smoother frequency curve, and higher overall performance. 

### Heatsinks

Whilst heatsinks are not necessary to prevent overheating damage to the SoC, the thermal throttling mechanisms handles that, if you wish to reduce the amount of thermal throttling that takes place, a heatsink or small fan will help. Depending on the exact circumstances, mounting the Pi vertically can also help with heat dissiapation as airflow can be improved.

### Measuring Temperature

Due to the architecture of the SoC's used ont he Raspberry Pi range, and the use in the Raspbian distribtution of the upstream temperature monitoring code, Linux based temperature measurements can be inaccurate. There is a gencmd which can provide an accurate and instantaneous reading of the current SoC temperature, as it communicates with the VC4 directly. 

```vcgencmd measure_temp```




