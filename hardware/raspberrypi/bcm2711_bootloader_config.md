# Pi 4 Bootloader Configuration

You can display the currently-active configuration using 
```
vcgencmd bootloader_config
```

To change these bootloader configuration items, you need to extract the configuration segment, make changes, re-insert it, then reprogram the EEPROM with the new bootloader. The Raspberry Pi will need to be rebooted for changes to take effect. 

```
# Copy the EEPROM image of interest from /lib/firmware/raspberrypi/bootloader/ to pieeprom.bin
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

## Configuration Properties
This section describes all the configuration items available in the bootloader. The syntax is the same as [config.txt](../../configuration/config-txt/) but the properties are specific to the bootloader. [Conditional filters](../../configuration/config-txt/conditional.md) are also supported except for EDID.

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

E.g. 0x21 means try SD first followed by network boot then stop. Whereas 0x2 would mean try network boot and then stop without trying to boot from the SD card.

The retry counters are reset when switching to the next boot mode.

BOOT_ORDER fields  
The BOOT_ORDER property defines the sequence for the different boot modes. It is read right to left and up to 8 digits may be defined.

* 0x0 - NONE (stop with error pattern)  
* 0x1 - SD CARD  
* 0x2 - NETWORK  
* 0x3 - USB device boot [usbboot](https://github.com/raspberrypi/usbboot) - Compute Module only.
* 0x4 - USB mass storage boot
* 0xf - RESTART (loop) - start again with the first boot order field.

Default: 0x1  
Version: pieeprom-2020-04-16.bin  

**pieeprom-2020-05-15.bin - BETA**
* Boot mode 0x0 will retry the SD boot if the SD card detect pin indicates that the card has been inserted or replaced.
* The default boot mode is now 0xf41 which means continuously try SD then USB mass storage.

### MAX_RESTARTS
If the RESTART (0xf) boot mode is encountered more than MAX_RESTARTS times then a watchdog reset is triggered. This isn't recommended for general use but may be useful for test or remote systems where a full reset is needed to resolve issues with hardware or network interfaces.

Default: -1 (infinite)  
Version: pieeprom-2020-05-15.bin - BETA  

### SD_BOOT_MAX_RETRIES
The number of times that SD boot will be retried after failure before moving to the next boot mode defined by `BOOT_ORDER`.  
-1 means infinite retries  
Default: 0  
Version: pieeprom-2020-04-16.bin  

### NET_BOOT_MAX_RETRIES
The number of times that network boot will be retried after failure before moving to the next boot mode defined by `BOOT_ORDER`.  
-1 means infinite retries  
Default: 0  
Version: pieeprom-2020-04-16.bin  

### DHCP_TIMEOUT
The timeout in milliseconds for the entire DHCP sequence before failing the current iteration.  
Default: 45000  
Minimum: 5000  
Version: pieeprom-2020-04-16.bin  

### DHCP_REQ_TIMEOUT
The timeout in milliseconds before retrying DHCP DISCOVER or DHCP REQ.  
Default: 4000  
Minimum: 500  
Version: pieeprom-2020-04-16.bin  

### TFTP_FILE_TIMEOUT
The timeout in milliseconds for an individual file download via TFTP.  
Default: 30000  
Minimum: 5000  
Version: pieeprom-2020-04-16.bin  

### TFTP_IP
Optional dotted decimal ip address (e.g. "192.168.1.99") for the TFTP server which overrides the server-ip from the DHCP request.  
This maybe useful on home networks because tftpd-hpa can be used instead of dnsmasq where broadband router is the DHCP server.

Default: ""  
Version: pieeprom-2020-04-16.bin  

### TFTP_PREFIX
In order to support unique TFTP boot directories for each Pi the bootloader prefixes the filenames with a device specific directory. If neither start4.elf nor start.elf are found in the prefixed directory then the prefix is cleared.
On earlier models the serial number is used as the prefix, however, on Pi 4 the MAC address is no longer generated from the serial number making it difficult to automatically create tftpboot directories on the server by inspecting DHCPDISCOVER packets. To support this the TFTP_PREFIX may be customized to either be the MAC address, a fixed value or the serial number (default).

* 0 - Use the serial number e.g. "9ffefdef/"
* 1 - Use the string specified by TFTP_PREFIX_STR
* 2 - Use the MAC address e.g. "DC-A6-32-01-36-C2/"

Default: 0  
Version: pieeprom-2020-04-16.bin  

### TFTP_PREFIX_STR
Specify the custom directory prefix string used when TFTP_PREFIX is set to 1. For example:- TFTP_PREFIX_STR=tftp_test/
Default: ""  
Version: pieeprom-2020-04-16.bin  

### PXE_OPTION43
Overrides the PXE Option43 match string with a different string. It's normally better to apply customisations to the DHCP server than change the client behaviour but this option is provided in case that's not possible.
Default: "Raspberry Pi Boot"  
Version: pieeprom-2020-04-16.bin  

### DHCP_OPTION97
In earlier releases the client GUID (Option97) was just the serial number repeated 4 times. By default, the new GUID format is
the concatenation of the fourcc for RPi4 (0x34695052 - little endian), the board revision (e.g. 0x00c03111) (4-bytes), the least significant 4 bytes of the mac address and the 4-byte serial number.
This is intended to be unique but also provide structured information to the DHCP server, allowing Raspberry Pi4 computers to be identified without relying upon the Ethernet MAC OUID.

Specify DHCP_OPTION97=0 to revert the the old behaviour or a non-zero hex-value to specify a custom 4-byte prefix.

Default: 0x34695052  
Version: pieeprom-2020-04-16.bin  

### Static IP address configuration
If TFTP_IP and the following options are set then DHCP is skipped and the static IP configuration is applied. If the TFTP server is on the same subnet as the client then GATEWAY may be omitted.

#### CLIENT_IP
The IP address of the client e.g. "192.168.0.32"   
Default: ""  
Version: pieeprom-2020-04-16.bin  

#### SUBNET
The subnet address mask e.g. "255.255.255.0"   
Default: ""  
Version: pieeprom-2020-04-16.bin  

#### GATEWAY
The gateway address to use if the TFTP server is on a differenet subnet e.g. "192.168.0.1"
Default: ""  
Version: pieeprom-2020-04-16.bin  

#### MAC_ADDRESS
Overrides the Ethernet MAC address with the given value. e.g. dc:a6:32:01:36:c2  
Default: ""   
Version: pieeprom-2020-04-16.bin

### DISABLE_HDMI
Disables the [HDMI boot diagnostics](./boot_diagnostics.md) display if a fatal error is encountered. This may also be disabled by setting `disable_splash=1` in config.txt.

N.B. By default, the HDMI diagnostics screen is automatically blanked after 2 minutes.
Default: 0  
Version: pieeprom-2020-04-16.bin  

`pieeprom-2020-05-15.bin - BETA`
The `disable_splash` property is no longer checked because the HDMI diagnostics screen is started before config.txt is read.

### ENABLE_SELF_UPDATE
Allows the bootloader to update itself instead of requiring recovery.bin. This is intended to make it easier to update the bootloader firmware via network boot. To enable set `ENABLE_SELF_UPDATE=1` and add `bootloader_update=1` in config.txt.
N.B. There is no automatic rollback in the event of a power failure during the firmware update. In the unlikely event of this happening you will have to use Pi Imager to apply the rescue image.

If self update is enabled then the bootloader will look for (pieeprom.upd + pieeprom.sig) and/or (vl805.bin + vl805.sig) on the boot partition (or TFTP root). If the update files are different to the current image then the update is applied and system is reset. Otherwise, if the images are identical then boot continues as normal.

Since the updates files are in the same format as generated by rpi-eeprom-update you can use rpi-eeprom-update to install the files to /boot so long as /boot mounts the approprate boot device / tftp-root (via NFS).

**The bootloader only reads the configuration from the bootconf.txt in the EEPROM and not the one in the update files. Therefore, in order to enable `ENABLE_SELF_UPDATE` you have to first update the bootloader via the SD-CARD or FLASHROM.**

Default: 0  
Version: pieeprom-2020-04-16.bin  

`pieeprom-2020-05-15.bin - BETA`
The `ENABLE_SELF_UPDATE` EEPROM property and `bootloader_update` config.txt property are now enabled by default so that `rpi-eeprom-update` may be used without requiring extra customization. Setting either of these parameters to zero prevents self-updates.

### FREEZE_VERSION
Previously this property was only checked by the rpi-eeprom-update script. However, now that self-update is enabled the bootloader will also check this property. If set, this overrides `ENABLE_SELF_UPDATE` to stop automatic updates. To disable `FREEZE_VERSION` you will have to use an SD card boot with recovery.bin.

Default: 0  
Version: pieeprom-2020-05-15.bin - BETA  

### BOOT_LOAD_FLAGS
Experimental property for custom firmware (bare metal).

Bit 0 (0x1) indicates that the .elf file is custom firmware. This disables any compatiblity checks (e.g. is USB MSD boot supported) and resets PCIe before starting the executable. 

### NETCONSOLE - advanced logging
`NETCONSOLE` duplicates debug messages to the network interface. The IP addresses and ports are defined by the `NETCONSOLE` string.

N.B. NETCONSOLE blocks until the ethernet link is established or a timeout occurs. The timeout value is `DHCP_TIMEOUT` although DHCP is not attempted unless network boot is requested.

#### Format
See https://wiki.archlinux.org/index.php/Netconsole
```
src_port@src_ip/dev_name,dst_port@tgt_ip/tgt_mac
E.g. 6665@169.254.1.1/eth0,6666@/
```
In order to simplify parsing, the bootloader requires every field separator to be present. In the example the target IP address (255.255.255.255) and target mac address (00:00:00:00:00) are assigned default values.

One way to view the data is to connect the test Pi 4 to another Pi running WireShark and select “udp.srcport == 6665” as a filter and select `Analyze -> Follow -> UDP stream` to view as an ASCII log.

`NETCONSOLE` should not be enabled by default because it may cause network problems. It can be enabled on demand via a GPIO filter e.g.
```
# Enable debug if GPIO 7 is pulled low
[gpio7=0]
BOOT_UART=1
NETCONSOLE=6665@169.254.1.1/eth0,6666@/
```

Version: pieeprom-2020-05-15.bin - BETA

## Network Boot
### Server configuration                                                    
Network boot requires a TFTP and NFS server to be configured.  See [Network boot server tutorial](bootmodes/net_tutorial.md)

Additional notes:-
* The MAC address on the Pi 4 is programmed at manufacture and is not derived from the serial number.
```                                                                          
# mac address (ip addr) - it should start with DC:A6:32
ip addr | grep ether | head -n1 | awk '{print $2}' | tr [a-z] [A-Z]                                                                                                                                                
# serial number                                                                                                                         
vcgencmd otp_dump | grep 28: | sed s/.*://g
```

### Installation - firmware update
Network boot is available in the latest production bootloader (pieeprom-2020-04-16.bin). Previous beta/stable releases which supported network boot are still available but are deprecated.

```
# Update the rpi-eeprom package                                                                                                 
sudo apt update
sudo apt upgrade
# Check the current version
sudo rpi-eeprom-update     
# Update to latest
sudo rpi-eeprom-update     
```

### Enable network boot
Network boot is not enabled by default in the bootloader. To enable it the bootloader configuration file must be edited.
```                                                                        
# Extract the configuration file                                                                                                         
cp /lib/firmware/raspberrypi/bootloader/critical/pieeprom-2020-04-16.bin pieeprom.bin                                                       
rpi-eeprom-config pieeprom.bin > bootconf.txt                                                                          
```
Change `BOOT_ORDER` to be `0x21` instead of `0x1`. This tells the bootloader to try sd-card boot first and network boot second. You should normally include sd-card (`0x1`) in the boot sequence in-case of network failure.

### Apply the configuration change to the EEPROM image file
```
rpi-eeprom-config --out pieeprom-netboot.bin --config bootconf.txt pieeprom.bin
```
### Install the new EEPROM image
```
sudo rpi-eeprom-update -d -f ./pieeprom-netboot.bin
sudo reboot
```

## USB mass storage boot
This is only available in the BETA release and requires updated firmware via [rpi-update](../../raspbian/applications/rpi-update.md). If you aren't already familiar with how to use a USB drive for the root filesystem then you probably want to wait until this feature is in the default Raspberry Pi OS image.

There is no support for migrating a SD card image to a USB drive. It is possible, but the process can potentially be quite involved and varies according to your original setup. Please see [this forum thread](https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=44177&start=350) for more information.

## BETA setup instructions
These instructions assume that you are familiar with manual firmware and bootloader updates and understand how to revert to a previous version if you want to revert the changes. If not, please wait until the features are available in a full Raspberry Pi OS release image.

### Check that the USB mass storage device works under Linux
Before attempting to boot from a USB mass storage device it is advisible to verify that the device works correctly under Linux. Boot using an SD card and plug in the USB mass storage device. This should appears as a removable drive.

This is especially important with USB SATA adapters which may be supported by the bootloader in mass storage mode but fail if Linux selects [USB Attached SCSI - UAS](https://en.wikipedia.org/wiki/USB_Attached_SCSI) mode. 

See this [forum thread](https://www.raspberrypi.org/forums/viewtopic.php?t=245931) about UAS and how to add [usb-storage.quirks](https://www.kernel.org/doc/html/v5.0/admin-guide/kernel-parameters.html) to workaround this issue.

### Update the bootloader
* From a standard Raspberry Pi OS SD card boot:
```
sudo apt update
sudo apt full-upgrade
```

* As root, edit `/etc/default/rpi-eeprom-update` and select BETA releases.

* Install the BETA version of the bootloader and replace the current configuration settings to enable USB boot.
See `BOOT_ORDER` property if you wish to migrate the configuration by hand.
```
sudo rpi-eeprom-update -d -f /lib/firmware/raspberrypi/bootloader/beta/pieeprom-2020-05-15.bin
```

* Reboot and check the bootloader version and config:
```
vcgencmd bootloader_version 
vcgencmd bootloader_config
```

### Create a bootable USB drive
* Use the [Raspberry Pi Imager](https://www.raspberrypi.org/downloads/) to flash Raspberry Pi OS to a USB mass storage device. Other distros have not been tested and may require updates (e.g. u-boot). One reason for having a public beta is to help get USB MSD boot support into other distros.
* Download the updated firmware files `*.elf *.dat` from the `master` branch of the [Raspberry Pi Firmware](https://github.com/raspberrypi/firmware) Github repo. 
* Alternatively use `sudo rpi-update` to update the firmware on a Raspberry Pi OS SD card install, then copy the files from there.
* Copy these updates to the boot partition on the USB device. From now on `sudo rpi-update` can be used from within Raspberry Pi OS on the USB boot device.
* A Linux kernel update is not required. Raspberry Pi OS has been tested using the 4.19 and 5.4 (32 and 64 bit) kernel.

### USB device compatiblity
There is no explicit set of supported devices. Initially we recommend using a USB pen drive or SSD. Hard drives will probably require a powered HUB and in all cases you should verify that the devices work correctly from within Raspberry Pi OS using an SD card boot.

Please post interoperability reports (positive or negative) on [this thread](https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=274595) on the Raspberry Pi forums. 

### USB_MSD_EXCLUDE_VID_PID
A list of up to 4 VID/PID pairs specifying devices which the bootloader should ignore. If this matches a HUB then the HUB won’t be enumerated, causing all downstream devices to be excluded.
This is intended to allow problematic (e.g. very slow to enumerate) devices to be ignored during boot enumeration. This is specific to the bootloader and is not passed to the OS.

The format is a comma-separated list of hexadecimal values with the VID as most significant nibble. Spaces are not allowed.
E.g. `034700a0,a4231234`

Default: “”  
Version: pieeprom-2020-05-15.bin - BETA    

### USB_MSD_DISCOVER_TIMEOUT
If no USB mass storage devices are found within this timeout then USB-MSD is stopped and the next boot mode is selected

Default: 20000 (20 seconds)  
Version: pieeprom-2020-05-15.bin - BETA  

### USB_MSD_BOOT_MAX_RETRIES
The number of times that USB MSD boot will be retried after failure before moving to the next boot mode defined by `BOOT_ORDER`.  
-1 means infinite retries  
Default: 0   
Version: pieeprom-2020-05-15.bin - BETA  

### USB_MSD_LUN_TIMEOUT
How long to wait in milliseconds before advancing to the next LUN e.g. a multi-slot SD-CARD reader. This is still being tweaked but may help speed up boot if old/slow devices are connected as well as a fast USB-MSD device containing the OS.

Default:  2000 (2 seconds)  
Version: pieeprom-2020-05-15.bin - BETA  

### XHCI_DEBUG
This property is a bit field which controls the verbosity of USB trace messages for mass storage boot mode. Enabling all of these messages generates a huge amount of log data which will slow down booting and may even cause boot to fail. For verbose logs it's best to use `NETCONSOLE`

* Bit 0 - USB descriptors
* Bit 1 - Mass storage mode state machine 
* Bit 2 - Mass storage mode state machine - verbose
* Bit 3 - All USB requests
* Bit 4 - Log device and hub state machines
* Bit 5 - Log all xHCI TRBs (VERY VERBOSE)
* Bit 6 - Log all xHCI events (VERY VERBOSE)

By default, no extra debug messages are enabled. 

```
# Example: Enable mass storage and USB descriptor logging
XHCI_DEBUG=0x3
```

Default: 0x0  
Version: pieeprom-2020-05-15.bin - BETA  

