# GPIO boot mode

The Raspberry Pi can be configured to allow the boot mode to be selected at power on using hardware attached to the GPIO connector: this is GPIO boot mode. This is done by setting bits in the OTP memory of the SoC. Once the bits are set, they permanently allocate 5 GPIOs to allow this selection to be made. Once the OTP bits are set they cannot be unset so you should think carefully about enabling this, since those 5 GPIO lines will then be unavailable for any other use.

To enable GPIO boot mode, add the following line to the config.txt file:

```
program_gpio_bootmode=n
```

Where n is the bank of GPIOs which you wish to use. Then reboot the Pi once to program the OTP with this setting. Bank 1 is GPIOs 22-26, bank 2 is GPIOs 39-43. Unless you have a Compute Module, you must use bank 1: the GPIOs in bank 2 are only available on the Compute Module. Because of the way the OTP bits are arranged, if you first program GPIO boot mode for bank 1, you then have the option of selecting bank 2 later. The reverse is not true: once bank 2 has been selected for GPIO boot mode, you cannot select bank 1.

Once GPIO boot mode is enabled, the Raspberry Pi will no longer boot. You must pull up at least one boot mode GPIO pin in order for the Pi to boot.

Once enabled, the GPIOs are allocated to boot modes as follows:

|Bank 1|Bank2|boot type|
|:----:|:---:|:-------:|
|22    |39   |SD0      |
|23    |40   |SD1      |
|24    |41   |NAND     |
|25    |42   |SPI      |
|26    |43   |USB      |

The various boot modes are attempted in the numerical order of the GPIO pins, i.e. SD0, then SD1, then NAND and so on.

SD1 is the Broadcom SD card / MMC interface, which is used by default for the built-in SD card slot, and on the Compute Module for the eMMC. SD1 is the Arasan SD card / MMC interface which is also capable of SDIO. All Raspberry Pi models with built-in wifi use SD1 to connect to the wifi chip via SDIO.

USB in the table is USB device boot mode and USB host boot mode, which are only available on certain models of Raspberry Pi.

The default pull resistance on the GPIO lines is 50K ohm, as documented on page 102 of the [BCM2835 ARM peripherals datasheet](hardware/raspberrypi/bcm2835/BCM2835-ARM-Peripherals.pdf). A pull resistance of 5K ohm is recommended to pull a GPIO line up: this will allow the GPIO to function but not consume too much power.
