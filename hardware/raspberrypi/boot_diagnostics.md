## Boot diagnostics on the Raspberry Pi 4 and 400

The bootloader EEPROM on the Pi 4 and 400 contains a diagnostic display which can be used to help troubleshoot certain types of boot problems. The diagnostic display is output on both HDMI ports, but only after a delay. This means it is not normally visible, however you can force it to be shown by booting the Pi with no boot device present. Note that early versions of the bootloader did not contain the diagnostic display.

![Boot Diagnostics Screen](bootloader-diagnostics.png)

This diagnostics page will also appear if the bootloader is unable to boot from an inserted SD card, or is unable to network boot; for example, if there is no bootable image on the card, or it is defective, or the network boot parameters are incorrect.

The top line describes the model of Pi and its memory capacity. The QR code is a link to the [Downloads Page](https://raspberrypi.org/downloads).

The diagnostic information is as follows:

| Line: | Information |
| ---- | ----------- |
| bootloader | Bootloader version,  build date |
| board      | Board revision, serial number, Ethernet MAC address | 
| boot       | Boot mode currently being attempted, boot order read from EEPROM config - see [boot order documentation](https://www.raspberrypi.org/documentation/hardware/raspberrypi/bcm2711_bootloader_config.md), RSTS: PM_RSTS register |
| SD         | SD card detected status, contents of CID (card identification) register |
| part	     | MBR partitions for boot mode currently being attempted |
| fw	       | Filename for start.elf and fixup.dat firmware, if present (e.g. start4x.elf, fixup4x.dat) |
| net	       | Network boot: link status (up/down), client IP address (ip), subnet (sn), default gateway (gw) |
| tftp       | Network boot: TFTP server IP address |


This display can be disabled using the DISABLE_HDMI option, see [Pi4 Bootloader Configuration](./bcm2711_bootloader_config.md).

**Note:** The boot diagnostic display is not an interactive bootloader. If you require an interactive bootloader, consider using a tool such as NOOBS or U-Boot.
