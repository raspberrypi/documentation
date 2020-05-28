# Network boot your Raspberry Pi

This tutorial is written to explain how to set up a simple DHCP/TFTP server which will allow you to boot a Raspberry Pi 3 from the network. The tutorial assumes that you have an existing home network, and that you want to use a Raspberry Pi for the **server**. You will need a second Raspberry Pi 3 as a **client** to be booted. Only one SD card is needed because the client will be booted from the server after the initial client configuration.

Due to the huge range of networking devices available, we can't guarantee that network booting will work with any device. We have had reports that, if you cannot get network booting to work, disabling STP frames on your network may help.

## Client configuration

This section only applies to the **original** Raspberry Pi 3B; if you are using the 3B+, then ignore this section and skip to the server section below then.

Before a Raspberry Pi will network boot, it needs to be booted from an SD card with a config option to enable USB boot mode. This will set a bit in the OTP (One Time Programmable) memory in the Raspberry Pi SoC that enables network booting. Once this is done, the SD card is no longer required. 

Install Raspberry Pi OS Lite (or Raspberry Pi OS with Raspberry Pi Desktop) on the SD card in the [usual way](../../../installation/installing-images/README.md). 

Afterwards, set up USB boot mode by preparing the `/boot` directory with the latest boot files:

```bash
sudo apt update && sudo apt full-upgrade
```

Now, enable USB boot mode with the following command:

```bash
echo program_usb_boot_mode=1 | sudo tee -a /boot/config.txt
```

This adds `program_usb_boot_mode=1` to the end of `/boot/config.txt`. Reboot the Raspberry Pi with `sudo reboot`. Once the client Raspberry Pi has rebooted, check that the OTP has been programmed with:

```
$ vcgencmd otp_dump | grep 17:
17:3020000a
```

Ensure the output `0x3020000a` is correct.

The client configuration is almost done. The final thing to do is to remove the `program_usb_boot_mode` line from `config.txt` (make sure there is no blank line at the end). You can do this with `sudo nano /boot/config.txt`, for example. Finally, shut the client Raspberry Pi down with `sudo poweroff`.

## Server configuration

Plug the SD card into the server Raspberry Pi, and then boot the server. Before you do anything else, make sure you have run `sudo raspi-config` and expanded the root file system to take up the entire SD card.

The client Raspberry Pi will need a root file system to boot off, so before you do anything else on the server, make a full copy of its file system and put it in a directory called `/nfs/client1`:

```bash
sudo mkdir -p /nfs/client1
sudo apt install rsync
sudo rsync -xa --progress --exclude /nfs / /nfs/client1
```

Regenerate SSH host keys on the client filesystem by chrooting into it:

```bash
cd /nfs/client1
sudo mount --bind /dev dev
sudo mount --bind /sys sys
sudo mount --bind /proc proc
sudo chroot .
rm /etc/ssh/ssh_host_*
dpkg-reconfigure openssh-server
exit
sudo umount dev sys proc
```

Find the settings of your local network. You need to find the address of your router (or gateway), which can be done with:

```bash
ip route | awk '/default/ {print $3}'
```

Then run:

```bash
ip -4 addr show dev eth0 | grep inet
```

which should give an output like:

```
inet 10.42.0.211/24 brd 10.42.0.255 scope global eth0
```

The first address is the IP address of your server Raspberry Pi on the network, and the part after the slash is the network size. It is highly likely that yours will be a `/24`. Also note the `brd` (broadcast) address of the network. Note down the output of the previous command, which will contain the IP address of the Raspberry Pi and the broadcast address of the network.

Finally, note down the address of your DNS server, which is the same address as your gateway. You can find this with:

```bash
cat /etc/resolv.conf
```

Configure a static network address on your server Raspberry Pi via the `systemd` networking, which works as the network handler and DHCP server.

To do that, you'll need to to create a `10-eth0.netdev` and a `11-eth0.network` like so:

```
sudo nano /etc/systemd/network/10-eth0.netdev
```

Add the following lines:

```
[Match]
Name=eth0

[Network]
DHCP=no
```

Then create a network file:

```
sudo nano /etc/systemd/network/11-eth0.network
```

Add the following contents:

```
[Match]
Name=eth0

[Network]
Address=10.42.0.211/24
DNS=10.42.0.1

[Route]
Gateway=10.42.0.1
```

At this point, you won't have working DNS, so you'll need to add the server you noted down before to `systemd/resolved.conf`. In this example, the gateway address is 10.42.0.1.

```bash
sudo nano /etc/systemd/resolved.conf
```

Uncomment the DNS line and add the DNS IP address there. Additionally, if you have a fallback DNS server, add it there as well.

```bash
[Resolve]
DNS=10.42.0.1
#FallbackDNS=
```

Enable `systemd-networkd` and then reboot for the changes to take effect:

```bash
sudo systemctl enable systemd-networkd
sudo reboot
```

Now start `tcpdump` so you can search for DHCP packets from the client Raspberry Pi:

```bash
sudo apt install tcpdump dnsmasq
sudo systemctl enable dnsmasq
sudo tcpdump -i eth0 port bootpc
```

Connect the client Raspberry Pi to your network and power it on. Check that the LEDs illuminate on the client after around 10 seconds, then you should get a packet from the client "DHCP/BOOTP, Request from ..."

```
IP 0.0.0.0.bootpc > 255.255.255.255.bootps: BOOTP/DHCP, Request from b8:27:eb...
```

Now you need to modify the `dnsmasq` configuration to enable DHCP to reply to the device. Press <kbd>CTRL + C</kbd> to exit the `tcpdump` program, then type the following:

```bash
echo | sudo tee /etc/dnsmasq.conf
sudo nano /etc/dnsmasq.conf
```

Then replace the contents of `dnsmasq.conf` with:

```
port=0
dhcp-range=10.42.0.255,proxy
log-dhcp
enable-tftp
tftp-root=/tftpboot
pxe-service=0,"Raspberry Pi Boot"
```

Where the first address of the `dhcp-range` line is, use the broadcast address you noted down earlier.

Now create a `/tftpboot` directory:

```bash
sudo mkdir /tftpboot
sudo chmod 777 /tftpboot
sudo systemctl enable dnsmasq.service
sudo systemctl restart dnsmasq.service
```

Now monitor the `dnsmasq` log:

```bash
tail -F /var/log/daemon.log
```

You should see something like this:

```
raspberrypi dnsmasq-tftp[1903]: file /tftpboot/bootcode.bin not found
```

Next, you will need to copy the contents of the boot folder into the `/tftpboot` directory.

First, press <kbd>CTRL + C</kbd> to exit the monitoring state. Then type the following: 

```bash
cp -r /boot/* /tftpboot
```

Since the tftp location has changed, restart `dnsmasq`:

```bash
sudo systemctl restart dnsmasq
```

### Set up NFS root

This should now allow your Raspberry Pi client to attempt to boot through until it tries to load a root file system (which it doesn't have).

At this point, export the `/nfs/client1` file system created earlier, and the TFTP boot folder.

```bash
sudo apt install nfs-kernel-server
echo "/nfs/client1 *(rw,sync,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports
echo "/tftpboot *(rw,sync,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports
```

Restart RPC-Bind and the NFS server in order to have them detect the new files.

```bash
sudo systemctl enable rpcbind
sudo systemctl restart rpcbind
sudo systemctl enable nfs-kernel-server
sudo systemctl restart nfs-kernel-server
```

Edit `/tftpboot/cmdline.txt` and from `root=` onwards, and replace it with:

```
root=/dev/nfs nfsroot=10.42.0.211:/nfs/client1,vers=4.1,proto=tcp rw ip=dhcp rootwait elevator=deadline
```

You should substitute the IP address here with the IP address you have noted down. Also remove any part of the command line starting with init=.

Finally, edit `/nfs/client1/etc/fstab` and remove the `/dev/mmcblk0p1` and `p2` lines (only `proc` should be left). Then, add the boot partition back in:
```
echo "10.42.0.211:/tftpboot /boot nfs defaults,vers=4.1,proto=tcp 0 0" | sudo tee -a /nfs/client1/etc/fstab
```

Good luck! If it doesn't boot on the first attempt, keep trying. It can take a minute or so for the Raspberry Pi to boot, so be patient.
