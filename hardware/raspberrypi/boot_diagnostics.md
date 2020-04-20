## Boot Diagnostics on the Raspberry Pi 4

The bootloader on the Raspberry Pi 4 is stored in EEPROM, and as well as providing boot services, is also capable of providing diagnostic information on an attached HDMI display. To display this information, remove the SD card from the Raspberry Pi 4, and reboot. A diagnostic display similar to below should appear on the attached display.

This diagnostics page will also appear if the bootloader is unable to boot from an inserted SD card, or is unable to network boot; for example, if there is no bootable image on the card, or it is defective, or the network boot parameters are incorrect.




The top line describes the Model of Pi and its memory capacity. The QR code is a link to the [Downloads Page](https://raspberrypi.org/downloads).

The diagnostic information is as follows:

| Line: | Information |
| ---- | ----------- |
| bootloader | Describes the the bootloader version the date it was built |
| board      | Board revision - Serial Number - Ethernet MAC address | 
| boot       | |
| SD CID	   | |
| part	     | |
| fw	       | |
| net	       | Status of networking - IP configuration (via DHCP)  IP address (ip), Subnet (sn), Default gateway (gw) |
| tftp       | |



