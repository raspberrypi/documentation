# Pi4 Bootloader Configuration

You can display the currently-active configuration using 
```
vcgencmd bootloader_config
```

To change these bootloader configuration items, you need to extract the configuration segment, make changes, re-insert it, then reprogram the EEPROM with the new bootloader. The Raspberry Pi will need to be rebooted for changes to take effect. 

```
# Extract the configuration file
cp /lib/firmware/raspberrypi/bootloader/stable/pieeprom-2020-01-17.bin pieeprom.bin
rpi-eeprom-config pieeprom.bin > bootconf.txt

# Edit the configuration using a text editor e.g. nano bootconf.txt

# Example change. If you have a UART cable then setting BOOT_UART=1 will help debug boot issues
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

### BOOT_UART

If 1 then enable UART debug output on GPIO 14 and 15. Configure the receiving debug terminal at 115200bps, 8 bits, no parity bits, 1 stop bit. 
Default: 0  
Version: All  

### WAKE_ON_GPIO 

If 1 then 'sudo halt' will run in a lower power mode until either GPIO3 or GLOBAL_EN are shorted to ground.  

Default: 0 in original version of bootloader (2019-05-10). Newer bootloaders have this set to 1.  
Version: All  

### POWER_OFF_ON_HALT  

If 1 and WAKE_ON_GPIO=0 then switch off all PMIC outputs in halt. This is lowest possible power state for halt but may cause problems with some HATs because 5V will still be on. GLOBAL_EN must be shorted to ground to boot.  

Default: 0  
Version: 2019-07-15  

### FREEZE_VERSION

If 1 then the `rpi-eeprom-update` will skip automatic updates on this board. The parameter is not processed by the EEPROM bootloader or recovery.bin since there is no way in software of fully write protecting the EEPROM. Custom EEPROM update scripts must also check for this flag.

Default: 0  
Version: All  

### BOOT_ORDER
The BOOT_ORDER setting allows flexible configuration for the priority of different bootmodes. It is represented as 32bit unsigned integer where each nibble represents a bootmode. The bootmodes are attempted in lowest significant nibble to highest significant nibble order.

E.g. 0x21 means try SD first followed by network boot then stop. Where as 0x2 would mean try network boot and then stop without trying to boot from the SD card.

The retry counters are reset when switching to the next boot mode.

BOOT_ORDER fields  
* 0x0 - NONE (stop with error pattern)  
* 0x1 - SD CARD  
* 0x2 - NETWORK  

Default: 0x00000001 (with 3 SD boot retries to match the current bootloader behaviour)  

### SD_BOOT_MAX_RETRIES
Specify the maximum number of times that the bootloader will retry booting from the SD card.  
-1 means infinite retries  
Default: 0  
Version: stable/pieeprom-2020-01-17.bin  

### NET_BOOT_MAX_RETRIES
Specify the maximum number of times that the bootloader will retry network boot.  
-1 means infinite retries  
Default: 0  
Version: stable/pieeprom-2020-01-17.bin  

### DHCP_TIMEOUT
The timeout in milliseconds for the entire DHCP sequence before failing the current iteration.  
Default: 45000  
Minimum: 5000  
Version: stable/pieeprom-2020-01-17.bin  

### DHCP_REQ_TIMEOUT
The timeout in milliseconds before retrying DHCP DISCOVER or DHCP REQ.  
Default: 4000  
Minimum: 500  
Version: stable/pieeprom-2020-01-17.bin  

### TFTP_TIMEOUT
The timeout in milliseconds for an individual file download via TFTP.  
Default: 15000  
Minimum: 5000  
Version: stable/pieeprom-2020-01-17.bin  

### TFTP_IP
Optional dotted decimal ip address (e.g. "192.168.1.99") for the TFTP server which overrides the server-ip from the DHCP request.  
This maybe useful on home networks because tftpd-hpa can be used instead of dnsmasq where broadband router is the DHCP server.
Default: ""  
Version: stable/pieeprom-2020-01-17.bin  

### TFTP_PREFIX
In order to support unique TFTP boot directories for each Pi the bootloader prefixes the filenames with a device specific directory. If neither start4.elf nor start.elf are found in the prefixed directory then the prefix is cleared.
On earlier models the serial number is used as the prefix, however, on Pi4 the MAC address is no longer generated from the serial number making it difficult to automatically create tftpboot directories on the server by inspecting DHCPDISCOVER packets. To support this the TFTP_PREFIX may be customized to either be the MAC address, a fixed value or the serial number (default).

* 0 - Use the serial number e.g. "9ffefdef/"
* 1 - Use the string specified by TFTP_PREFIX_STR
* 2 - Use the MAC address e.g. "DC-A6-32-01-36-C2/"
Default: 0  
Version: stable/pieeprom-2020-01-17.bin  

### TFTP_PREFIX_STR
Specify the custom directory prefix string used when TFTP_PREFIX is set to 1. For example:- TFTP_PREFIX_STR=tftp_test/
Default: ""  
Version: stable/pieeprom-2020-01-17.bin  

### PXE_OPTION43
Overrides the PXE Option43 match string with a different string. It's normally better to apply customisations to the DHCP server than change the client behaviour but this option is provided in case that's not possible.
Default: "Raspberry Pi Boot"  
Version: stable/pieeprom-2020-03-19.bin  

### DHCP_OPTION97
In earlier releases the client GUID (Option97) was just the serial number repeated 4 times. By default, the new GUID format is
the concatenation of the fourcc for RPi4 (0x34695052 - little endian), the board revision (e.g. 0x00c03111) (4-bytes), the least significant 4 bytes of the mac address and the 4-byte serial number.
This is intended to be unique but also provide structured information to the DHCP server, allowing Raspberry Pi4 computers to be identified without relying upon the Ethernet MAC OUID.

Specify DHCP_OPTION97=0 to revert the the old behaviour or a non-zero hex-value to specify a custom 4-byte prefix.

Default: 0x34695052
Version: stable/pieeprom-2020-03-19.bin  

### Static IP address configuration
If TFTP_IP and the following options are set then DHCP is skipped and the static IP configuration is applied. If the TFTP server is on the same subnet as the client then GATEWAY may be omitted.

#### CLIENT_IP
The IP address of the client e.g. "192.168.0.32"
Default: ""  
Version: stable/pieeprom-2020-03-19.bin  

#### SUBNET
The subnet address mask e.g. "255.255.255.0"
Default: ""  
Version: stable/pieeprom-2020-03-19.bin  

#### GATEWAY
The gateway address to use if the TFTP server is on a differenet subnet e.g. "192.168.0.1"
Default: ""  
Version: stable/pieeprom-2020-03-19.bin  

### DISABLE_HDMI
Disables the HDMI boot diagnostics display if a fatal error is encountered. This may also be disabled by setting display_splash=1 in config.txt.
N.B. By default, the HDMI diagnostics screen is automatically blanked after 2 minutes.
Default: 0  
Version: stable/pieeprom-2020-03-19.bin  

### SELF_UPDATE
Allows the bootloader to update itself instead of requiring recovery.bin. This is intended to make it easier to update the bootloader firmware via network boot. To enable set SELF_UPDATE=1 and add bootloader_update=1 in config.txt.
N.B. There is no automatic rollback in the event of a power failure during the firmware update. In the unlikely event of this happening you will have to use Pi Imager to apply the rescue image.

If self update is enabled then the bootloader will look for (pieeprom.upd + pieeprom.sig) and/or (vl805.bin + vl805.sig) on the boot partition (or TFTP root). If the update files are different to the current image then the update is applied and system is reset. Otherwise, if the images are identical then boot continues as normal.

Since the updates files are in the same format as generated by rpi-eeprom-update you can use rpi-eeprom-update to install the files to /boot so long as /boot mounts the approprate boot device / tftp-root (via NFS).

Default: 0  
Version: stable/pieeprom-2020-03-19.bin  

## Network Boot
### Server configuration                                                    
Network boot requires a TFTP and NFS server to be configured.  See [Network boot server tutorial](bootmodes/net_tutorial.md)

Additional notes:-
* The MAC address on the Pi4 is programmed at manufacture and is not derived from the serial number.
```                                                                          
# mac address (ip addr) - it should start with DC:A6:32
ip addr | grep ether | head -n1 | awk '{print $2}' | tr [a-z] [A-Z]                                                                                                                                                
# serial number                                                                                                                         
vcgencmd otp_dump | grep 28: | sed s/.*://g
```

### Installation - firmware update
Network boot functionality requires the 2020-02-13 Raspbian Buster release (or newer) and an updated bootloader. For advanced boot modes (USB, network) it is normally best to use the latest 'stable' bootloader.

```
# Update the rpi-eeprom package                                                                                                 
sudo apt update
sudo apt upgrade
                                                                          
# Network boot is only available in the stable and beta releases.
# Switch from critical updates to the stable release series.
# As root:-
echo FIRMWARE_RELEASE_STATUS="stable" > /etc/default/rpi-eeprom-update
```

### Enable network boot
Network boot is not enabled by default in the bootloader. To enable it the bootloader configuration file must be edited.
```                                                                        
# Extract the configuration file                                                                                                         
cp /lib/firmware/raspberrypi/bootloader/stable/pieeprom-2020-01-17.bin pieeprom.bin                                                       
rpi-eeprom-config pieeprom.bin > bootconf.txt                                                                          
```
Change BOOT_ORDER to be 0x21 instead of 0x1. This tells the bootloader to try sd-card boot first and network boot second. You should normally include sd-card (0x1) in the boot sequence in-case of network failure.

### Apply the configuration change to the EEPROM image file
```
rpi-eeprom-config --out pieeprom-netboot.bin --config bootconf.txt pieeprom.bin
```
### Install the new EEPROM image
```
sudo rpi-eeprom-update -d -f ./pieeprom-netboot.bin
sudo reboot
```
