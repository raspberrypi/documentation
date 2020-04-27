## Boot Diagnostics on the Raspberry Pi 4

The bootloader on the Raspberry Pi 4 is stored in EEPROM, and as well as providing boot services, is also capable of providing diagnostic information on an attached HDMI display. To display this information, remove the SD card from the Raspberry Pi 4, and reboot. A diagnostic display similar to below should appear on the attached display.

This diagnostics page will also appear if the bootloader is unable to boot from an inserted SD card, or is unable to network boot; for example, if there is no bootable image on the card, or it is defective, or the network boot parameters are incorrect.

This information screen is displayed only after a reboot caused by a power cycle, not a software instigated reboot.

The top line describes the model of Pi and its memory capacity. The QR code is a link to the [Downloads Page](https://raspberrypi.org/downloads).

The diagnostic information is as follows:

| Line: | Information |
| ---- | ----------- |
| bootloader | Bootloader version - build date |
| board      | Board revision - Serial Number - Ethernet MAC address | 
| boot       | mode: (ROM boot mode - 6 SPI), order: EEPROM config [BOOT_ORDER](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bcm2711_bootloader_config.md), RSTS: PM_RSTS register |
| SD CID	   | SD Card Identifier defined by SD-CARD manufacture |
| part	     | Master Boot Record primary partitions type:LBA |
| fw	       | Filename for start.elf and fixup.dat if present (e.g. start4x.dat, fixup4x.dat) |
| net	       | Network boot: - Link status (up/down) client IP address (ip), Subnet (sn), Default gateway (gw) |
| tftp       | Network boot: TFTP server IP address|


This display can be disabled using the DISABLE_HDMI option, see [Pi4 Bootloader Configuration](./bcm2711_bootloader_config.md).

N.B. This is purely for diagnosing boot failures, this is not an interactive bootloader. That operation is performed later on in the boot by NOOBs / U-BOOT etc.

