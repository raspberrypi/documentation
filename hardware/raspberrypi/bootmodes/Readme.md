# IMPORTANT
This is preliminary information used by the beta testers for the development of the bootcode for mass storage and ethernet boot, but it is currently incorrect and not working.  If you'd like to join the beta test then please send your email to @gsholling on Twitter and I'll invite you to the Slack channel which we're using to discuss this...


# Raspberry Pi boot modes

## Introduction

The Raspberry Pi has a number of different stages of booting, this document is meant to help explain how the boot modes work, which ones are supported for Linux booting and how they work.

## Boot flow

The flow of boot begins with reading the OTP to decide on the valid boot modes enabled.  By default this is SD card boot followed by USB device boot.  Subsequently the bootrom checks to see if `program_gpio_bootmode` OTP bit is set, if it is then it reads either GPIOs 22-26 or 39-43 (depending on the value of `program_gpio_bootpos`) and uses those bits to disable boot modes.  This means it is possible to use a hardware switch to switch between different boot modes if there are more than one available.

Next the boot rom checks each of the boot sources for a file called bootcode.bin if it is successfull then it will load the code into the local 128K cache and jump to it.

* Primary SD card boot
* Secondary SD card boot
* NAND boot (currently not supported for Linux booting)
* SPI EEPROM boot (currently not supported for Linux booting)
* USB boot
  * If device mode is set then boot as device
  * If host mode is also set then use OTG bit to decide (Pi B has host enabled)

The primary SD card boot mode is as standard set to be GPIOs 49-53 it is possible (although we've not yet enabled) the ability to boot from the secondary SD card on a second set of pins (i.e. to add a secondary SD card to the GPIO pins).

NAND boot and SPI boot modes do work, although they do not yet have full GPU support.

The USB will boot as a USB device (when plugged into a PC for example) so you can 'squirt' the bootcode.bin into the device.  The code for doing this is [usbboot](https://github.com/raspberrypi/tools/tree/master/usbboot).

Also 2837 has the additional capability to boot as a USB host, if both modes are enabled then the OTG pin on the device is used to select between device and host.  For the Pi 3 this is wired to ground which turns the Pi into a host, but CM3 based designs should use the OTG pin to switch between device and host boot if this is required.

## USB host boot

The USB host boot was a mode added with 2837 (Raspberry Pi 3) it requires that an OTP bit is blown to enable the mode and can be done by adding `program_usb_boot_mode=1` to config.txt

Once this has been done the following will occur:

* 2837 boots
* Reads bootrom enabled boot modes
* Uses gpio_bootmode to disable some modes by reading GPIOs 22-26 or 39-43 to see if the default values do not equal the default pull.  If it is default it will disable that boot mode for each of SD1, SD2, NAND, SPI, USB
* If enabled: Check primary SD for bootcode.bin
  * Success - Boot
  * Fail - timeout (5 seconds)
* If enabled: Check secondary SD
  * Sucess - Boot
  * Fail - timeout (5 seconds)
* If enabled: Check NAND
* If enabled: Check SPI
* If enabled: Check USB
  * Enable USB, wait for valid USB 2.0 devices (2 seconds)
    * Device found:
      * If device type == hub
        * Recurse for each port
      * If device type == (mass storage or LAN9500)
        * Store in list of devices
  * Recurse through each MSD
    * If bootcode.bin found boot
  * Recurse through each LAN9500
    * DHCP / TFTP boot

NOTES: 

* If there is no SD card inserted the SD boot mode takes 5 seconds to fail, to reduce this and fall back to USB quicker you can either insert an SD card with nothing on it or use the `program_gpio_bootmode` OTP to specifically only enable USB.
* USB enumeration is a mechanism of enabling the power to the downstream devices on a hub then waiting for the devices to pull the D+ and D- lines to indicate it is either USB 1 or USB 2.  This can take time and on some devices it can take up to 3 seconds for a hard disk drive to spin up and start the enumeration process.  Because this is the only way of detecting the hardware is attached we have to sit waiting for a minimum amount of time (2 seconds) if the device fails to respond after this maximum timeout it is possible to increase the timeout to 5 seconds using program_usb_timeout=1 in config.txt
* MSD takes precedence over ethernet boot
* It is no longer necessary for the first partition to be the FAT partition, the MSD boot will continue to search for a FAT partition beyond the first one.
* The bootrom also now supports GUID partitioning and has been tested with hard drives partitioned using Mac, Windows and Linux.

# Network booting

To network boot the bootrom does the following:

* Initialise LAN9500
* Send DHCP request
* Receive DHCP reply
* (optional) Receive DHCP proxy reply
* ARP to tftpboot server
* ARP reply includes tftpboot server ethernet address
* TFTP RRQ 'bootcode.bin'
  * File not found: Server replies with TFTP error response with textual error message
  * File exists: Server will reply with the first block (512 bytes) of data for the file with a block number in the header
    * Pi replys with TFTP ACK packet containing the block number, repeats until the last block which is not 512 bytes
* TFTP RRQ 'bootsig.bin'
  * This will normally result in an error file not found...

From this point the bootcode.bin code continues to load the system, the first file it will try to access is [`serial_number`]/start.elf if this does __not__ result in a error then any other files to be read will be pre-pended with the `serial_number`.  This is useful because if enables you to create separate directories with separate start.elf / kernels for your Pis
To get the serial number for the device you can either try this boot mode and see what file is accessed using tcpdump / wireshark or you can run a standard Raspbian SD card and `cat /proc/cpuinfo`

If you put all your files into the root of your tftp directory then all following files will be accessed from there.

# Setting up a DHCP / TFTP server

This tutorial is written to explain how to set up a simple DHCP / TFTP server to boot a Raspberry Pi 3 from the network.  This first tutorial assumes you only have a Raspberry Pi for the SERVER and a Pi 3 as a CLIENT to be booted.

Install a standard Raspbian lite (or heavy if you want) from the [Downloads page](https://www.raspberrypi.org/downloads/raspbian/) onto an SD card using whatever process you like (dd or Win32DiskImager or something similar).  Before booting the Client edit the config.txt and add the following to config.txt

```
program_usb_boot_mode=1
```

Now copy [start.elf](start.elf) and [bootcode.bin](bootcode.bin) to the sdcard overwriting the currently existing start.elf and bootcode.bin, you should also:

```
rm start_* fixup*
```

Plug the SD card into the CLIENT and boot it with a keyboard and HDMI connected.  When it boots, log in and check that the OTP is correctly programmed

```
$ vcgencmd otp_dump | grep 17:
17:3020000a
```

Make sure the 0x3020000a is correct.

Now, shutdown the Pi gracefully and re-edit the config.txt file to remove the `program_usb_boot_mode` (you don't actually have to do this, it will enable USB boot modes but shouldn't break anything.)

Plug the SD card into the SERVER and boot the server, with it connected to the internet install some useful applications:

```
sudo apt-get install tcpdump
sudo apt-get install dnsmasq
sudo apt-get remove dhcpcd
```

After this we'll need to fix DNS because dnsmasq breaks it a bit...

```
sudo rm /etc/resolvconf/update.d/dnsmasq
sudo reboot
```

Now Take an ethernet cable and plug it directly between the SERVER and the CLIENT and set a static IP address on the SERVER:

```
sudo ifconfig eth0 down
sudo ifconfig eth0 up 192.168.1.1 netmask 255.255.255.0 broadcast 192.168.1.255
sudo tcpdump -i eth0
```
Now power the CLIENT

Check that the LEDs illuminate on the CLIENT after around 10 seconds, then you get a packet from the CLIENT "DHCP/BOOTP, Request from ..."

Now we need to modify the dnsmasq configuration to enable DHCP to reply to the device ...

```
sudo echo | sudo tee /etc/dnsmasq.conf
sudo nano /etc/dnsmasq.conf
```

Then replace the contents of dnsmasq.conf with:

```
port=0
log-dhcp
enable-tftp
tftp-root=/tftpboot
dhcp-range=eth0,192.168.1.100,192.168.1.150,12h
pxe-service=0,"Raspberry Pi Boot"
```

It's important that the 192.168.1.x matches the subnet you used in the static IP settings, the range is what it'll share

Now create a /tftpboot directory

```
$ sudo mkdir /tftpboot
$ sudo chmod 777 /tftpboot
$ sudo systemctl restart dnsmasq.service
```

Next we can try the tcpdump again...

```
sudo tcpdump -i eth0
```

You should see a DHCP REPLY packet and a TFTP read request packet, for "bootcode.bin"

Next, you will need to copy [bootcode.bin](bootcode.bin) and [start.elf](start.elf) into the /tftpboot directory, you should be able to do this by just copying the files from /boot since they are the right ones...

```
cp /boot/bootcode.bin /tftpboot
cp /boot/start.elf /tftpboot
```

Now when you power off and then power on the CLIENT tcpdump should give lots of data (you should also notice the LEDs flashing for longer when it boots).


