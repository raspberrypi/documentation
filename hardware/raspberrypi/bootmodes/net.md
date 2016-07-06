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
echo "denyinterfaces eth0" | sudo tee -a /etc/dhcpcd.conf
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

Now when you power off and then power on the CLIENT tcpdump should give lots of data and the result should be the green LED flashing (this means it couldn't find the kernel, not surprising since we didn't give it one...)

Next, we need to provide the other files (kernel and dt overlays etc) which are currently stored on the SERVER's boot directory, so:

```
cp -r /boot/* /tftpboot
```

This should now allow your Pi to boot through until it tried to load a root filesystem (which it doesn't have)...  This is the point where you need to provide a filing system which is beyond this tutorial... Although I'll give you some clues for sharing the SERVERS filesystem with the client...

* Reboot SERVER with a normal ethernet connection (you'll probably need to remove the dhcpcd.conf line to re-enable the client)
* `sudo apt-get install nfs-kernel-server`
* `sudo vi /etc/exports`
* Add the line "/ *(rw,sync,no_subtree_check)" to exports
* sudo systemctl restart rpcbind.service
* sudo systemctl restart nfs-kernel-server.service
* Reboot with the ethernet connected to the CLIENT and do the static IP thing again
* Check the mount is working using something like `sudo mount 192.168.1.1:/ tmp`
* edit /tftpboot/cmdline.txt and change to
  * "root=/dev/nfs nfsroot=192.168.1.1:/ rw ip=dhcp rootwait"
* edit /etc/fstab and remove the /dev/mmcblkp1 and p2 lines
* edit /boot/cmdline.txt (the SERVER's cmdline) and add "rw" to the line

Think that's it... Good luck...
