# GPIO boot mode

The Raspberry Pi can be configured to allow the boot mode to be selected at run time using hardware attached to the GPIO connector: this is GPIO boot mode. This is done by setting a bit in the OTP memory of the SoC. Once the bit is set, it permanently allocates 5 GPIOs to allow this selected to be made. Once the OTP bit is set it cannot be undone, so you should think carefully about enabling this, since those 5 GPIO lines will then be permanently unavailable for any other use.

To enable GPIO boot mode, add the following line to the config.txt file:

```
program_gpio_bootmode=n
```

And reboot the Pi once to program the OTP with this setting. Where n is the bank of GPIOs which you wish to use. Bank 1 is GPIOs 22-26, bank 2 is GPIOs 39-43. Unless you have a compute module, you must use bank 1: the GPIOs in bank 2 are only available on the compute module.

Once GPIO boot mode is enabled, the Raspberry Pi will no longer boot. You must pull up at least one boot mode GPIO pin in order for the Pi to boot.

Once enabled, the GPIOs are mapped as follows:

|Bank 1|Bank2|boot type|
|:----:|:---:|:-------:|
|22    |39   |SD1      |
|23    |40   |SD2      |
|24    |41   |NAND     |
|25    |42   |SPI      |
|26    |43   |USB      |

SD1 is the <xxx> SD card interface. SD2 is the <yyy> SD card interface. USB enables both USB device mode and USB host mode boot.

The default pull resistance on the GPIO lines is 50K ohm, so a pull resistance of 5K ohm should suffice but still enable the GPIO to be operational but not consume a lot of power.
