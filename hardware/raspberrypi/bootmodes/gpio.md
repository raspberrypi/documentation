# GPIO boot mode

The Raspberry Pi can be configured to allow the boot mode to be selected at power on using hardware attached to the GPIO connector: this is GPIO boot mode. This is done by setting bits in the OTP memory of the SoC. Once the bits are set, they permanently allocate 5 GPIOs to allow this selection to be made. Once the OTP bits are set they cannot be unset so you should think carefully about enabling this, since those 5 GPIO lines will then be unavailable for any other use.

To enable GPIO boot mode, add the following line to the [config.txt](../../../configuration/config-txt/README.md) file:

```
program_gpio_bootmode=n
```

Where n is the bank of GPIOs which you wish to use. Then reboot the Pi once to program the OTP with this setting. Bank 0 is GPIOs 22-26, bank 1 is GPIOs 39-43. Unless you have a Compute Module, you must use bank 0: the GPIOs in bank 1 are only available on the Compute Module. Because of the way the OTP bits are arranged, if you first program GPIO boot mode for bank 0, you then have the option of selecting bank 1 later. The reverse is not true: once bank 1 has been selected for GPIO boot mode, you cannot select bank 0.

Once GPIO boot mode is enabled, the Raspberry Pi will no longer boot. You must pull up at least one boot mode GPIO pin in order for the Pi to boot.

Once enabled, the GPIOs are allocated to boot modes as follows:

|Bank 1|Bank 2|boot type|
|:----:|:---:|:---- ---:|
|22    |39   |SD0       |
|23    |40   |SD1       |
|24    |41   |NAND (no Linux support at present)      |
|25    |42   |SPI (no Linux support at present)      |
|26    |43   |USB       |

The various boot modes are attempted in the numerical order of the GPIO pins, i.e. SD0, then SD1, then NAND and so on.

SD0 is the Broadcom SD card / MMC interface. When the boot ROM within the SoC runs, it always connects SD0 to the built-in SD card slot, or on the Compute Module, to the eMMC device. SD1 is the Arasan SD card / MMC interface which is also capable of SDIO. All Raspberry Pi models with built-in wifi use SD1 to connect to the wifi chip via SDI0.

It is possible to reassign both SD0 and SD1 to different uses after the Pi has booted, but the boot ROM will always use the assignments noted above at boot time .

USB in the table selects USB device boot mode and USB host boot mode, which are only available on certain models of Raspberry Pi. In order to use a USB boot mode, it must by enabled in the OTP memory. For more information, see [USB device boot](device.md) and [USB host boot](host.md)

The default pull resistance on the GPIO lines is 50K ohm, as documented on page 102 of the [BCM2835 ARM peripherals datasheet](../../hardware/raspberrypi/bcm2835/BCM2835-ARM-Peripherals.pdf). A pull resistance of 5K ohm is recommended to pull a GPIO line up: this will allow the GPIO to function but not consume too much power.
