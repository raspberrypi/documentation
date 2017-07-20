# Network booting

This section describes how network booting works. There is also a [tutorial](net_tutorial.md) available on setting up a working bootable system. Network booting works only for the wired adapter. Booting over wireless LAN is not supported.

To network boot, the boot ROM does the following:

* Initialise LAN9500
* Send DHCP request
* Receive DHCP reply
* (optional) Receive DHCP proxy reply
* ARP to tftpboot server
* ARP reply includes tftpboot server ethernet address
* TFTP RRQ 'bootcode.bin'
  * File not found: Server replies with TFTP error response with textual error message
  * File exists: Server will reply with the first block (512 bytes) of data for the file with a block number in the header
    * Pi replies with TFTP ACK packet containing the block number, and repeats until the last block which is not 512 bytes
* TFTP RRQ 'bootsig.bin'
  * This will normally result in an error `file not found`. This is to be expected, and TFTP boot servers should be able to handle it.

From this point the `bootcode.bin` code continues to load the system. The first file it will try to access is [`serial_number`]/start.elf. If this does not result in a error then any other files to be read will be pre-pended with the `serial_number`. This is useful because it enables you to create separate directories with separate start.elf / kernels for your Pis
To get the serial number for the device you can either try this boot mode and see what file is accessed using tcpdump / wireshark, or you can run a standard Raspbian SD card and `cat /proc/cpuinfo`.

If you put all your files into the root of your tftp directory then all following files will be accessed from there.

## Debugging the NFS boot mode

The first thing to check is that the OTP bit is correctly programmed. To do this, you need to add `program_usb_boot_mode=1` to config.txt and reboot (with a standard SD card that boots correctly into Raspbian). Once you've done this, you should be able to do:

```
$ vcgencmd otp_dump | grep 17:
17:3020000a
```

If row 17 contains that value then the OTP is correctly programmed. You should now be able to remove the SD card, plug in Ethernet,
and then the Ethernet LEDs should light up around 5 seconds after the Pi powers up.

To capture the ethernet packets on the server, use tcpdump on the tftpboot server (or DHCP server if they are different). You will need to capture the packets there otherwise you will not be able to see packets that get sent directly because network switches are not hubs!

``` 
sudo tcpdump -i eth0 -w dump.pcap
```

This will write everything from eth0 to a file dump.pcap you can then post process it or upload it to cloudshark.com for communication

### DHCP Request / Reply

As a minimum you should see a DHCP request and reply which looks like the following:

```
6:44:38.717115 IP (tos 0x0, ttl 128, id 0, offset 0, flags [none], proto UDP (17), length 348)
    0.0.0.0.68 > 255.255.255.255.67: [no cksum] BOOTP/DHCP, Request from b8:27:eb:28:f6:6d, length 320, xid 0x26f30339, Flags [none] (0x0000)
	  Client-Ethernet-Address b8:27:eb:28:f6:6d
	  Vendor-rfc1048 Extensions
	    Magic Cookie 0x63825363
	    DHCP-Message Option 53, length 1: Discover
	    Parameter-Request Option 55, length 12: 
	      Vendor-Option, Vendor-Class, BF, Option 128
	      Option 129, Option 130, Option 131, Option 132
	      Option 133, Option 134, Option 135, TFTP
	    ARCH Option 93, length 2: 0
	    NDI Option 94, length 3: 1.2.1
	    GUID Option 97, length 17: 0.68.68.68.68.68.68.68.68.68.68.68.68.68.68.68.68
	    Vendor-Class Option 60, length 32: "PXEClient:Arch:00000:UNDI:002001"
	    END Option 255, length 0
16:44:41.224619 IP (tos 0x0, ttl 64, id 57713, offset 0, flags [none], proto UDP (17), length 372)
    192.168.1.1.67 > 192.168.1.139.68: [udp sum ok] BOOTP/DHCP, Reply, length 344, xid 0x26f30339, Flags [none] (0x0000)
	  Your-IP 192.168.1.139
	  Server-IP 192.168.1.1
	  Client-Ethernet-Address b8:27:eb:28:f6:6d
	  Vendor-rfc1048 Extensions
	    Magic Cookie 0x63825363
	    DHCP-Message Option 53, length 1: Offer
	    Server-ID Option 54, length 4: 192.168.1.1
	    Lease-Time Option 51, length 4: 43200
	    RN Option 58, length 4: 21600
	    RB Option 59, length 4: 37800
	    Subnet-Mask Option 1, length 4: 255.255.255.0
	    BR Option 28, length 4: 192.168.1.255
	    Vendor-Class Option 60, length 9: "PXEClient"
	    GUID Option 97, length 17: 0.68.68.68.68.68.68.68.68.68.68.68.68.68.68.68.68
	    Vendor-Option Option 43, length 32: 6.1.3.10.4.0.80.88.69.9.20.0.0.17.82.97.115.112.98.101.114.114.121.32.80.105.32.66.111.111.116.255
	    END Option 255, length 0
```

The important part of the reply is the Vendor-Option Option 43. This needs to contain the string "Raspberry Pi Boot", although, due
to a bug in the boot ROM, you may need to add three spaces to the end of the string.

### TFTP file read

You will know whether the Vendor Option is correctly specified: if it is, you'll see a subsequent TFTP RRQ packet being sent. RRQs can be replied to by either the first block of data or an error saying file not found. In a couple of cases they even receive the first packet and then the transmission is aborted by the Pi (this happens when checking whether a file exists). The example below is just three packets: the original read request, the first data block (which is always 516 bytes containing a header and 512 bytes of data, although the last block is always less than 512 bytes and may be zero length), and the third packet (the ACK which contains a frame number to match the frame number in the data block).

```
16:44:41.224964 IP (tos 0x0, ttl 128, id 0, offset 0, flags [none], proto UDP (17), length 49)
    192.168.1.139.49152 > 192.168.1.1.69: [no cksum]  21 RRQ "bootcode.bin" octet 
16:44:41.227223 IP (tos 0x0, ttl 64, id 57714, offset 0, flags [none], proto UDP (17), length 544)
    192.168.1.1.55985 > 192.168.1.139.49152: [udp sum ok] UDP, length 516
16:44:41.227418 IP (tos 0x0, ttl 128, id 0, offset 0, flags [none], proto UDP (17), length 32)
    192.168.1.139.49152 > 192.168.1.1.55985: [no cksum] UDP, length 4
```

See Also:
* [Network boot tutorial](net_tutorial.md)
