# Raspberry Pi 4 bootloader configuration

## Editing the configuration
Before editing the bootloader configuration, [update your system](../../raspbian/updating.md) to get the latest version of the `rpi-eeprom` package.  Releases prior to the 2020-09-03 default/critical release will not support all features listed here.

To view the current EEPROM configuration:  
`rpi-eeprom-config`

To edit it and apply the updates to latest EEPROM release:  
`sudo -E rpi-eeprom-config --edit`

Please see the [boot EEPROM](booteeprom.md) page for more information about the EEPROM update process.

## Configuration properties
This section describes all the configuration items available in the bootloader. The syntax is the same as [config.txt](../../configuration/config-txt/README.md) but the properties are specific to the bootloader. [Conditional filters](../../configuration/config-txt/conditional.md) are also supported except for EDID.

<a name="BOOT_UART"></a>
### BOOT_UART

If `1` then enable UART debug output on GPIO 14 and 15. Configure the receiving debug terminal at 115200bps, 8 bits, no parity bits, 1 stop bit.

Default: `0`  

<a name="WAKE_ON_GPIO"></a>
### WAKE_ON_GPIO

If `1` then `sudo halt` will run in a lower power mode until either GPIO3 or GLOBAL_EN are shorted to ground.

Default: `1` (`0` in original version of bootloader 2019-05-10)  

<a name="POWER_OFF_ON_HALT"></a>
### POWER_OFF_ON_HALT

If `1` and `WAKE_ON_GPIO=0` then `sudo halt` will switch off all PMIC outputs. This is lowest possible power state for halt but may cause problems with some HATs because 5V will still be on. `GLOBAL_EN` must be shorted to ground to boot.

Pi 400 has a dedicated power button which operates even if the processor is switched off. This behaviour is enabled by default, however, `WAKE_ON_GPIO=2` may be set to use an external GPIO power button instead of the dedicated power button.

Default: `0`  

<a name="BOOT_ORDER"></a>
### BOOT_ORDER
The `BOOT_ORDER` setting allows flexible configuration for the priority of different boot modes. It is represented as 32bit unsigned integer where each nibble represents a boot mode. The boot modes are attempted in lowest significant nibble to highest significant nibble order.

The minimum supported bootloader version for custom boot modes is 2020-09-03.

##### `BOOT_ORDER` fields
The BOOT_ORDER property defines the sequence for the different boot modes. It is read right to left and up to 8 digits may be defined.

| Value | Mode            | Description                                                                                                                     |
|-------|-----------------|---------------------------------------------------------------------------------------------------------------------------------|
|  0x0  |  SD CARD DETECT |  Try SD then wait for card-detect to indicate that the card has changed - deprecated now that 0xf (RESTART) is available.       |
|  0x1  |  SD CARD        |  SD card (or eMMC on Compute Module 4).                                                                                         |
|  0x2  |  NETWORK        |  Network boot - See [Network boot server tutorial](bootmodes/net_tutorial.md)                                                   |
|  0x3  |  RPIBOOT        |  RPIBOOT - See [usbboot](https://github.com/raspberrypi/usbboot)                                                                |
|  0x4  |  USB-MSD        |  USB mass storage boot - See [USB mass storage boot](bootmodes/msd.md)                                                          |
|  0x5  |  BCM-USB-MSD    |  USB 2.0 boot from USB Type C socket (CM4: USB type A socket on CM IO board, using bootloader EEPROM from 2020-12-14 onwards).  |
|  0x6  |  NVME           |  CM4 only: boot from an NVMe SSD connected to the PCIe interface. See [NVMe boot](bootmodes/nvme.md) for more details.          |
|  0xe  |  STOP           |  Stop and display error pattern. A power cycle is required to exit this state.                                                  |
|  0xf  |  RESTART        |  Restart from the first boot-mode in the BOOT_ORDER field i.e. loop                                                             |

`RPIBOOT` is intended for use with Compute Module 4 to load a custom debug image (e.g. a Linux RAM-disk) instead of the normal boot. This should be the last boot option because it does not currently support timeouts or retries.

##### `BOOT_ORDER` examples

| BOOT_ORDER | Description                                                                    |
| -----------|--------------------------------------------------------------------------------|
| 0xf41      | Try SD first, followed by USB-MSD then repeat (default if BOOT_ORDER is empty) |
| 0xf14      | Try USB first, followed by SD then repeat                                      |
| 0xf21      | Try SD first, followed by NETWORK then repeat                                  |

<a name="MAX_RESTARTS"></a>
### MAX_RESTARTS
If the RESTART (`0xf`) boot mode is encountered more than MAX_RESTARTS times then a watchdog reset is triggered. This isn't recommended for general use but may be useful for test or remote systems where a full reset is needed to resolve issues with hardware or network interfaces.

Default: `-1` (infinite)  

<a name="SD_BOOT_MAX_RETRIES"></a>
### SD_BOOT_MAX_RETRIES
The number of times that SD boot will be retried after failure before moving to the next boot mode defined by `BOOT_ORDER`.  
`-1` means infinite retries.

Default: `0`  

<a name="NET_BOOT_MAX_RETRIES"></a>
### NET_BOOT_MAX_RETRIES
The number of times that network boot will be retried after failure before moving to the next boot mode defined by `BOOT_ORDER`.  
`-1` means infinite retries.

Default: `0`  

<a name="DHCP_TIMEOUT"></a>
### DHCP_TIMEOUT
The timeout in milliseconds for the entire DHCP sequence before failing the current iteration.

Minimum: `5000`  
Default: `45000`  

<a name="DHCP_REQ_TIMEOUT"></a>
### DHCP_REQ_TIMEOUT
The timeout in milliseconds before retrying DHCP DISCOVER or DHCP REQ.

Minimum: `500`  
Default: `4000`  

<a name="TFTP_FILE_TIMEOUT"></a>
### TFTP_FILE_TIMEOUT
The timeout in milliseconds for an individual file download via TFTP.

Minimum: `5000`  
Default: `30000`  

<a name="TFTP_IP"></a>
### TFTP_IP
Optional dotted decimal ip address (e.g. `192.168.1.99`) for the TFTP server which overrides the server-ip from the DHCP request.  
This may be useful on home networks because tftpd-hpa can be used instead of dnsmasq where broadband router is the DHCP server.

Default: ""  

<a name="TFTP_PREFIX"></a>
### TFTP_PREFIX
In order to support unique TFTP boot directories for each Pi the bootloader prefixes the filenames with a device specific directory. If neither start4.elf nor start.elf are found in the prefixed directory then the prefix is cleared.
On earlier models the serial number is used as the prefix, however, on Pi 4 the MAC address is no longer generated from the serial number making it difficult to automatically create tftpboot directories on the server by inspecting DHCPDISCOVER packets. To support this the TFTP_PREFIX may be customized to either be the MAC address, a fixed value or the serial number (default).

| Value | Description                                   |
|-------|-----------------------------------------------|
| 0     | Use the serial number e.g. `9ffefdef/`        |
| 1     | Use the string specified by TFTP_PREFIX_STR   |
| 2     | Use the MAC address e.g. `dc-a6-32-01-36-c2/` |

Default: 0  

<a name="TFTP_PREFIX_STR"></a>
### TFTP_PREFIX_STR
Specify the custom directory prefix string used when `TFTP_PREFIX` is set to 1. For example:- `TFTP_PREFIX_STR=tftp_test/`

Default: ""  
Max length: 32 characters  

<a name="PXE_OPTION43"></a>
### PXE_OPTION43
Overrides the PXE Option43 match string with a different string. It's normally better to apply customisations to the DHCP server than change the client behaviour but this option is provided in case that's not possible.

Default: `Raspberry Pi Boot`  

<a name="DHCP_OPTION97"></a>
### DHCP_OPTION97
In earlier releases the client GUID (Option97) was just the serial number repeated 4 times. By default, the new GUID format is
the concatenation of the fourcc for RPi4 (0x34695052 - little endian), the board revision (e.g. 0x00c03111) (4-bytes), the least significant 4 bytes of the mac address and the 4-byte serial number.
This is intended to be unique but also provide structured information to the DHCP server, allowing Raspberry Pi4 computers to be identified without relying upon the Ethernet MAC OUID.

Specify DHCP_OPTION97=0 to revert the the old behaviour or a non-zero hex-value to specify a custom 4-byte prefix.

Default: `0x34695052`  

### Static IP address configuration
If TFTP_IP and the following options are set then DHCP is skipped and the static IP configuration is applied. If the TFTP server is on the same subnet as the client then GATEWAY may be omitted.

<a name="CLIENT_IP"></a>
#### CLIENT_IP
The IP address of the client e.g. `192.168.0.32`

Default: ""  

<a name="SUBNET"></a>
#### SUBNET
The subnet address mask e.g. `255.255.255.0`

Default: ""  

<a name="GATEWAY"></a>
#### GATEWAY
The gateway address to use if the TFTP server is on a differenet subnet e.g. `192.168.0.1`

Default: ""  

<a name="MAC_ADDRESS"></a>
#### MAC_ADDRESS
Overrides the Ethernet MAC address with the given value. e.g. `dc:a6:32:01:36:c2`

Default: ""  

<a name="DISABLE_HDMI"></a>
### DISABLE_HDMI
The [HDMI boot diagnostics](boot_diagnostics.md) display is disabled if `DISABLE_HDMI=1`. Other non-zero values are reserved for future use.

Default: `0`  

<a name="HDMI_DELAY"></a>
### HDMI_DELAY
Skip rendering of the HDMI diagnostics display for up to N seconds (default 5) unless a fatal error occurs. The default behaviour is designed to avoid the bootloader diagnostics screen from briefly appearing during a normal SD / USB boot.

Default: `5`  

<a name="ENABLE_SELF_UPDATE"></a>
### ENABLE_SELF_UPDATE
Enables the bootloader to update itself from a TFTP or USB mass storage device (MSD) boot filesystem.

If self update is enabled then the bootloader will look for the update files (.sig/.upd) in the boot file system. If the update image differs from the current image then the update is applied and system is reset. Otherwise, if the EEPROM images are byte-for-byte identical then boot continues as normal.

Notes:-
* Self-update is not enabled in SD boot; the ROM can already load recovery.bin from the SD card.
* Before self-update can be used the bootloader must have already been updated to a version which supports self update. The recommended approach would be to use the Raspberry Pi Imager and a spare SD card to update to pieeprom-2020-09-03 then use self-update for subsequent updates.
* For network boot make sure that the TFTP `boot` directory can be mounted via NFS and that `rpi-eeprom-update` can write to it.

Default: `1` (`0` in versions prior to 2020-09-03)  

<a name="FREEZE_VERSION"></a>
### FREEZE_VERSION
Previously this property was only checked by the `rpi-eeprom-update` script. However, now that self-update is enabled the bootloader will also check this property. If set to 1, this overrides `ENABLE_SELF_UPDATE` to stop automatic updates. To disable `FREEZE_VERSION` you will have to use an SD card boot with recovery.bin.

**Custom EEPROM update scripts must also check this flag.**

Default: `0`  

<a name="NETCONSOLE"></a>
### NETCONSOLE - advanced logging
`NETCONSOLE` duplicates debug messages to the network interface. The IP addresses and ports are defined by the `NETCONSOLE` string.

N.B. NETCONSOLE blocks until the ethernet link is established or a timeout occurs. The timeout value is `DHCP_TIMEOUT` although DHCP is not attempted unless network boot is requested.

#### Format
See https://wiki.archlinux.org/index.php/Netconsole
```
src_port@src_ip/dev_name,dst_port@dst_ip/dst_mac
E.g. 6665@169.254.1.1/,6666@/
```
In order to simplify parsing, the bootloader requires every field separator to be present. The source ip address must be specified but the following fields may be left blank and assigned default values.

* src_port - 6665
* dev_name - "" (the device name is always ignored)
* dst_port - 6666
* dst_ip - 255.255.255.255
* dst_mac - 00:00:00:00:00

One way to view the data is to connect the test Pi 4 to another Pi running WireShark and select “udp.srcport == 6665” as a filter and select `Analyze -> Follow -> UDP stream` to view as an ASCII log.

`NETCONSOLE` should not be enabled by default because it may cause network problems. It can be enabled on demand via a GPIO filter e.g.
```
# Enable debug if GPIO 7 is pulled low
[gpio7=0]
NETCONSOLE=6665@169.254.1.1/,6666@/
```

Default: ""  (not enabled)  
Max length: 32 characters  

<a name="USB_MSD_EXCLUDE_VID_PID"></a>
### USB_MSD_EXCLUDE_VID_PID
A list of up to 4 VID/PID pairs specifying devices which the bootloader should ignore. If this matches a HUB then the HUB won’t be enumerated, causing all downstream devices to be excluded.
This is intended to allow problematic (e.g. very slow to enumerate) devices to be ignored during boot enumeration. This is specific to the bootloader and is not passed to the OS.

The format is a comma-separated list of hexadecimal values with the VID as most significant nibble. Spaces are not allowed.
E.g. `034700a0,a4231234`

Default: ""  

<a name="USB_MSD_DISCOVER_TIMEOUT"></a>
### USB_MSD_DISCOVER_TIMEOUT
If no USB mass storage devices are found within this timeout then USB-MSD is stopped and the next boot mode is selected

Default: `20000` (20 seconds)  
Version: 2020-09-03  

<a name="USB_MSD_LUN_TIMEOUT"></a>
### USB_MSD_LUN_TIMEOUT
How long to wait in milliseconds before advancing to the next LUN e.g. a multi-slot SD-CARD reader. This is still being tweaked but may help speed up boot if old/slow devices are connected as well as a fast USB-MSD device containing the OS.

Default: `2000` (2 seconds)  

<a name="USB_MSD_PWR_OFF_TIME"></a>
### USB_MSD_PWR_OFF_TIME
During USB mass storage boot, power to the USB ports is switched off for a short time to ensure the correct operation of USB mass storage devices. Most devices work correctly using the default setting: change this only if you have problems booting from a particular device. Setting `USB_MSD_PWR_OFF_TIME=0` will prevent power to the USB ports being switched off during USB mass storage boot.

Minimum: `250`  
Maximum: `5000`  
Default: `1000` (1 second)  

<a name="XHCI_DEBUG"></a>
### XHCI_DEBUG
This property is a bit field which controls the verbosity of USB debug messages for mass storage boot mode. Enabling all of these messages generates a huge amount of log data which will slow down booting and may even cause boot to fail. For verbose logs it's best to use `NETCONSOLE`.

| Value | Log                                       |
|-------|-------------------------------------------|
|  0x1  | USB descriptors                           |
|  0x2  | Mass storage mode state machine           |
|  0x4  | Mass storage mode state machine - verbose |
|  0x8  | All USB requests                          |
|  0x10 | Device and hub state machines             |
|  0x20 | All xHCI TRBs (VERY VERBOSE)              |
|  0x40 | All xHCI events (VERY VERBOSE)            |

To combine values, add them together. For example: 
```
# Enable mass storage and USB descriptor logging
XHCI_DEBUG=0x3
```

Default: `0x0` (no USB debug messages enabled)  

## config.txt - configuration properties

<a name="boot_load_flags"></a>
### boot_load_flags
Experimental property for custom firmware (bare metal).

Bit 0 (0x1) indicates that the .elf file is custom firmware. This disables any compatibility checks (e.g. is USB MSD boot supported) and resets PCIe before starting the executable.

Default: `0x0`  

<a name="uart_2ndstage"></a>
### uart_2ndstage
If set to 0x1 then enable debug logging to the UART. In newer firmware versions (Raspberry Pi OS 2020-08-20 and later) UART logging is also automatically enabled in start.elf. This is also described on the [Boot options](../../configuration/config-txt/boot.md) page.

The `BOOT_UART` property also enables bootloader UART logging but does not enable UART logging in `start.elf` unless `uart_2ndstage=1` is also set.

Default: `0`  

<a name="eeprom_write_protect"></a>
### eeprom_write_protect
The `2020-09-03` `recovery.bin` EEPROM updater provides a feature to configure the EEPROM `Write Status Register`. This can be set to either mark the entire EEPROM as write-protected or clear write-protection.

This option must be used in conjunction with the EEPROM `/WP` pin which controls updates to the EEPROM `Write Status Register`.  Pulling `/WP` low (CM4 `EEPROM_nEP` or Pi4B `TP5`) does NOT write-protect the EEPROM unless the `Write Status Register` has also been configured.

See: [Winbond W25x40cl datasheet](https://www.winbond.com/resource-files/w25x40cl_f%2020140325.pdf)

`eeprom_write_protect` settings in `config.txt` for `recovery.bin`.

| Value | Description                                                      |
|-------|------------------------------------------------------------------|
|  1    | Configures the write protect regions to cover the entire EEPROM. |
|  0    | Clears the write protect regions.                                |
| -1    | Do nothing.                                                      |

N.B `flashrom` does not support clearing of the write-protect regions and will fail to update the EEPROM if write-protect regions are defined.

Default: `-1`  

<a name="bootloader_update"></a>
### bootloader_update
This option may be set to 0 to block self-update without requiring the EEPROM configuration to be updated. This is sometimes useful when updating multiple Pis via network boot because this option can be controlled per Raspberry Pi (e.g. via a serial number filter in `config.txt`).

Default: `1` (`0` in versions prior to 2020-09-03)  

<a name="config_txt"></a>
### config.txt section
From Raspberry Pi OS 2021-01-11, the firmware now reads the bootloader configuration from the EEPROM. If a section called `[config.txt]` is found then the contents from the start of this section to the end of the file is appended in memory, to the contents of the `config.txt` file read from the boot partition.  This can be used to automatically apply settings to every operating system, for example, dtoverlays.

If an invalid configuration which causes boot to fail is specified then an EEPROM recovery image or RPIBOOT will be required to restore the EEPROM to factory defaults.

