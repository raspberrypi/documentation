# Pi4 Bootloader Configuration (BETA)

To change bootloader configuration items, you need to extract the configuration segment, make changes, re-insert it, then reprogram the EEPROM with the new bootloader. 

```
# Extract the configuration file
cp /lib/firmware/raspberrypi/bootloader/beta/pieeprom-2019-09-23.bin pieeprom.bin
rpi-eeprom-config pieeprom.bin > bootconf.txt

# Edit the configuration using a text editor e.g. nano bootconf.txt

# E.G. change boot_order from 0x1 (sd-boot) to network 0x20, then SD (0x01)
BOOT_ORDER=0x21

# If you have a UART cable then setting BOOT_UART=1 will help debug boot issues
BOOT_UART=1

# Save the new configuration and exit editor

# Apply the configuration change to the EEPROM image file
rpi-eeprom-config --out pieeprom-new.bin --config bootconf.txt pieeprom.bin
```

To update the bootloader EEPROM with the edited bootloader:

```
# Flash the bootloader EEPROM
# Run 'rpi-eeprom-update -h' for more information
sudo rpi-eeprom-update -d -f ./pieeprom-new.bin
sudo reboot
```

## Configuration Items

This section describes all the configuration items available in the bootloader.

### BOOT_ORDER
The BOOT_ORDER setting allows flexible configuration for the priority of different
bootmodes. It is represented as 32bit unsigned integer where each nibble represents
a bootmode. The bootmodes are attempted in LSB to MSB order.  

E.g. 0x21 means try SD first followed by network boot then stop. Where as
0x2 would mean try network boot and then stop without trying to boot from
the sd-card.

The retry counters are reset when switching to the next boot mode.

BOOT_ORDER fields  
* 0x0 - NONE (stop with error pattern)  
* 0x1 - SD CARD  
* 0x2 - NETWORK  

Default: 0x00000001 (with 3 SD boot retries to match the current bootloader behaviour)  

### SD_BOOT_MAX_RETRIES
Specify the maximum number of times that the bootloader will retry booting from the sd-card.  
-1 means infinite retries  
Default: 0  

### NET_BOOT_MAX_RETRIES
Specify the maximum number of times that the bootloader will retry network boot.  
-1 means infinite retries  
Default: 0  

### DHCP_TIMEOUT
The timeout in milliseconds for the entire DHCP sequence before failing the current iteration.  
Default: 45000  
Minimum: 5000  

### DHCP_REQ_TIMEOUT
The timeout in milliseconds before retrying DHCP DISCOVER or DHCP REQ.  
Default: 4000  
Minimum: 500  

### TFTP_TIMEOUT
The timeout in milliseconds for an individual file download via TFTP.  
Default: 15000  
Minimum: 5000  

### TFTP_IP
Optional dotted decimal ip address (e.g. 192.169.1.99) for the TFTP server which overrides the server-ip from the DHCP request.  
This maybe useful on home networks because tftpd-hpa can be used instead of dnsmasq where broadband router is the DHCP server.
Default: ""  
