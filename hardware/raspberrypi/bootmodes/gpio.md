# GPIO boot mode

**GPIO boot mode is only available on the Raspberry Pi 3A+, 3B, 3B+, Compute Module 3 and 3+**

The Raspberry Pi can be configured to allow the boot mode to be selected at power on using hardware attached to the GPIO connector: this is GPIO boot mode. This is done by setting bits in the OTP memory of the SoC. Once the bits are set, they permanently allocate 5 GPIOs to allow this selection to be made. Once the OTP bits are set they cannot be unset so you should think carefully about enabling this, since those 5 GPIO lines will always control booting. Although you can use the GPIOs for some other function once the Pi has booted, you must set them up so that they enable the desired boot modes when the Pi boots.

To enable GPIO boot mode, add the following line to the [config.txt](../../../configuration/config-txt/README.md) file:

```
program_gpio_bootmode=n
```

Where n is the bank of GPIOs which you wish to use. Then reboot the Pi once to program the OTP with this setting. Bank 1 is GPIOs 22-26, bank 2 is GPIOs 39-43. Unless you have a Compute Module, you must use bank 1: the GPIOs in bank 2 are only available on the Compute Module. Because of the way the OTP bits are arranged, if you first program GPIO boot mode for bank 1, you then have the option of selecting bank 2 later. The reverse is not true: once bank 2 has been selected for GPIO boot mode, you cannot select bank 1.

Once GPIO boot mode is enabled, the Raspberry Pi will no longer boot. You must pull up at least one boot mode GPIO pin in order for the Pi to boot.

## GPIO boot mode pin assignments
### Raspberry Pi 3B and Compute Module 3

|Bank 1|Bank 2|boot type|
|:----:|:---:|:--------:|
|22    |39   |SD0       |
|23    |40   |SD1       |
|24    |41   |NAND (no Linux support at present)    |
|25    |42   |SPI (no Linux support at present)    |
|26    |43   |USB       |

USB in the table above selects both USB device boot mode and USB host boot mode. In order to use a USB boot mode, it must by enabled in the OTP memory. For more information, see [USB device boot](device.md) and [USB host boot](host.md).

### Raspberry Pi 3A+, 3B+ and Compute Module 3+

|Bank 1|Bank 2|boot type|
|:----:|:---:|:--------:|
|20    |37   |SD0       |
|21    |38   |SD1       |
|22    |39   |NAND (no Linux support at present)    |
|23    |40   |SPI (no Linux support at present)    |
|24    |41   |USB device      |
|25    |42   |USB host - mass storage device |
|26    |43   |USB host - ethernet |

## Boot order

The various boot modes are attempted in the numerical order of the GPIO lines, i.e. SD0, then SD1, then NAND and so on.

## Boot flow

SD0 is the Broadcom SD card / MMC interface. When the boot ROM within the SoC runs, it always connects SD0 to the built-in microSD card slot. On Compute Modules with an eMMC device, SD0 is connected to that; on the Compute Module Lite SD0 is available on the edge connector and connects to the microSD card slot in the CMIO carrier board. SD1 is the Arasan SD card / MMC interface which is also capable of SDIO. All Raspberry Pi models with built-in wireless LAN use SD1 to connect to the wireless chip via SDIO.

The default pull resistance on the GPIO lines is 50K ohm, as documented on page 102 of the [BCM2835 ARM peripherals datasheet](../../hardware/raspberrypi/bcm2835/BCM2835-ARM-Peripherals.pdf). A pull resistance of 5K ohm is recommended to pull a GPIO line up: this will allow the GPIO to function but not consume too much power.
