# Network Boot Your Raspberry Pi
This tutorial is written to explain how to set up a simple DHCP / TFTP server which will allow you to boot a Raspberry Pi 3 from the network. The tutorial assumes you have an existing home network, and want to use a Raspberry Pi for the **server**. You will need a second Pi 3 as a **client** to be booted. Only one SD card is needed because the **client** will be booted from the **server** after the initial client configuration.

## Client configuration
Before a Pi will network boot, it needs to be booted with a config option to enable USB boot mode. Enabling this config option requires a special `start.elf` and `bootcode.bin` file. These can be installed by using the "next" branch on rpi-update.

Install Raspbian lite (or heavy if you want) from the [Downloads page](https://www.raspberrypi.org/downloads/raspbian/) onto an SD card using `Win32DiskImager` if you are on Windows, or `dd` if you are on Linux/Mac. Boot the **client** Pi.

### Program USB Boot Mode
First, prepare the `/boot` directory with experimental boot files:
```
# If on raspbian lite you need to install rpi-update before you can use it:
$ sudo apt-get update; sudo apt-get install rpi-update
$ sudo BRANCH=next rpi-update
```

Then enable USB boot mode with:
```
echo program_usb_boot_mode=1 | sudo tee -a /boot/config.txt
```

This adds `program_usb_boot_mode=1` to the end of `/boot/config.txt`. Reboot the Pi with `sudo reboot`. Once the client Pi has rebooted, check that the OTP is has been programmed with:

```
$ vcgencmd otp_dump | grep 17:
17:3020000a
```

Ensure the output `0x3020000a` is correct.

The client configuration is almost done. The final thing to do is to remove the `program_usb_boot_mode` line from config.txt (make sure there is no blank line at the end). You can do this with `sudo nano /boot/config.txt` for example. Finally, shut down the client Pi with `sudo poweroff`.

## Server configuration
Plug the SD card into the **server** and boot the server. Before you do anything else, make sure you have ran `sudo raspi-config` and expanded the root filesystem to take up the entire SD card.

The client Pi will need a root filesystem to boot off, so before we do anything else on the server, we're going to make a full copy of its filesystem and put it in a directory called /nfs/client1.

```
sudo mkdir -p /nfs/client1
sudo apt-get install rsync
sudo rsync -xa --progress --exclude /nfs / /nfs/client1
```

Regenerate ssh host keys on client filesystem by chrooting into it:
```
cd /nfs/client1
sudo mount --bind /dev dev
sudo mount --bind /sys sys
sudo mount --bind /proc proc
sudo chroot .
rm /etc/ssh/ssh_host_*
dpkg-reconfigure openssh-server
exit
sudo umount dev
sudo umount sys
sudo umount proc
```

You need to find the settings of your local network. You need to find the address of your router (or gateway), which you can find with:
```
ip route | grep default | awk '{print $3}'
```

Then run:

```
ip -4 addr show dev eth0 | grep inet
```

which should give an output like:

```
inet 10.42.0.211/24 brd 10.42.0.255 scope global eth0
```

The first address is the IP address of your server Pi on the network, and the part after the slash is the network size. It is highly likely that yours will be a `/24`. Also note the `brd` (broadcast) address of the network. Note down the output of the previous command, which will contain the IP address of the Pi and the Broadcast address of the network.

Finally note down the address of your DNS server, which is the same address as your gateway. You can find this with:
```
cat /etc/resolv.conf
```

Configure a static network adddress on your server Pi by with `sudo nano /etc/network/interfaces` (where you replace nano with an editor of your choice). Change the line, `iface eth0 inet manual` so that the address is the first address from the command before last, the netmask address as `255.255.255.0` and the gateway address as the number received from the last command. 

```
auto eth0
iface eth0 inet static 
        address 10.42.0.2
        netmask 255.255.255.0
        gateway 10.42.0.1
```

Then disable the DHCP client daemon and switch to standard Debian networking:
```
sudo systemctl disable dhcpcd
sudo systemctl enable networking
```

Reboot for the changes to take effect:
```
sudo reboot
```

At this point, you won't have working DNS, so you'll need to add the server you noted down before to `/etc/resolv.conf`. Do this by using the following command, where the ip address is that of the gateway address you found before.

```
echo "nameserver 10.42.0.1" | sudo tee -a /etc/resolv.conf
```

Then make the file immutable (because otherwise dnsmasq will interfere) with the following command:
```
sudo chattr +i /etc/resolv.conf
```

Then install software we need:
```
sudo apt-get update
sudo apt-get install dnsmasq tcpdump
```

Stop dnsmasq breaking DNS resolving:
```
sudo rm /etc/resolvconf/update.d/dnsmasq
sudo reboot
```

Now start tcpdump so you can search for DHCP packets from the client Pi:

```
sudo tcpdump -i eth0 port bootpc
```

Connect the client Pi to your network and power it on. Check that the LEDs illuminate on the client after around 10 seconds, then you should get a packet from the client "DHCP/BOOTP, Request from ..."

```
IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from b8:27:eb...
```

Now we need to modify the dnsmasq configuration to enable DHCP to reply to the device. Press `CTRL+C` on the keyboard to exit the tcpdump program, then type the following:

```
sudo echo | sudo tee /etc/dnsmasq.conf
sudo nano /etc/dnsmasq.conf
```

Then replace the contents of dnsmasq.conf with:

```
port=0
dhcp-range=10.42.0.255,proxy
log-dhcp
enable-tftp
tftp-root=/tftpboot
pxe-service=0,"Raspberry Pi Boot"
```

Where the first address of the `dhcp-range` line is, use the broadcast address you noted down earlier.

Now create a /tftpboot directory:

```
sudo mkdir /tftpboot
sudo chmod 777 /tftpboot
sudo systemctl enable dnsmasq.service
sudo systemctl restart dnsmasq.service
```

Now monitor the dnsmasq log:

```
tail -f /var/log/daemon.log
```

You should see something like this:
```
raspberrypi dnsmasq-tftp[1903]: file /tftpboot/bootcode.bin not found
```

Next, you will need to copy `bootcode.bin` and `start.elf` into the /tftpboot directory; you should be able to do this by just copying the files from /boot since they are the right ones. We need a kernel, so we might as well copy the entire boot directory.

First, use Ctrl+Z to exit the monitoring state. Then type the following: 

```
cp -r /boot/* /tftpboot
```

Restart dnsmasq for good measure:
```
sudo systemctl restart dnsmasq
```

### Set up NFS root
This should now allow your Pi to boot through until it tries to load a root filesystem (which it doesn't have). All we have to do to get this working is to export the `/nfs/client1` filesystem we created earlier.

```
sudo apt-get install nfs-kernel-server
echo "/nfs/client1 *(rw,sync,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports
sudo systemctl enable rpcbind
sudo systemctl restart rpcbind
sudo systemctl enable nfs-kernel-server
sudo systemctl restart nfs-kernel-server
```

Edit /tftpboot/cmdline.txt and from `root=` onwards, replace it with:

```
root=/dev/nfs nfsroot=10.42.0.2:/nfs/client1 rw ip=dhcp rootwait elevator=deadline
```

You should substitute the IP address here with the IP address you have noted down.

Finally, edit /nfs/client1/etc/fstab and remove the /dev/mmcblkp1 and p2 lines (only proc should be left).

Good luck! If it doesn't boot first time keep trying. It can take a minute or so for the Pi to boot, so be patient.
