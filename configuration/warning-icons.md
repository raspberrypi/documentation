# Firmware warning icons

Under certain circumstances, the Raspberry Pi firmware will display a warning icon on the display, to indicate an issue.

There are currently three icons that can be displayed.

## Undervoltage warning

If the power supply to the Raspberry Pi drops below 4.63V (+/-5%), the following icon is displayed.

![Under Voltage](images/under_volt.png)

## Over temperature warning (80-85C)

If the temperature of the SoC is between 80C and 85C, the following icon is displayed. The ARM core(s) will be throttled back in an attempt to reduce the core temperature.

![Over Temperature (80-85C)](images/over_temperature_80_85.png)

## Over temperature warning (over 85C)

If the temperature of the SoC is over 85C, the following icon is displayed. The ARM core(s) and the GPU will be throttled back in an attempt to reduce the core temperature.

![Over Temperature (85C+)](images/over_temperature_85.png)
